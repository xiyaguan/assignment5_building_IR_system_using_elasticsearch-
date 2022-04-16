from flask import Flask, render_template, request, session
from flask_session import Session
from elasticsearch_dsl.connections import connections
from evaluate import get_response
from collections import defaultdict

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

INDEX_NAME = "wapo_docs_50k"
DOC_PER_PAGE = 8
K = 20
SHOW_REL = False
TRUNCATE_LENGTH = 150
connections.create_connection(hosts=["localhost"], timeout=100, alias="default")


# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    keywords_text = request.form["keywords"]
    session["query_text"] = query_text
    session["keywords_text"] = keywords_text

    if query_text == "" and keywords_text == "":
        return home()

    option_analyzer = request.form['options_analyzer'] if 'options_analyzer' in request.form else 'standard_analyzer'
    option_embed = request.form['options_embed'] if 'options_embed' in request.form else 'bm25'

    session["option_analyzer"] = option_analyzer
    session["option_embed"] = option_embed

    use_standard_analyzer = (option_analyzer == "standard_analyzer")

    response = get_response(INDEX_NAME, query_text, keywords_text, use_standard_analyzer, option_embed, K)
    session["response"] = response
    items = [hit for hit in response[: DOC_PER_PAGE]]

    contents = {hit.meta.id: hit.content for hit in response[: DOC_PER_PAGE]}
    page_num = (len(response) - 1) // 8 + 1
    session["page_num"] = page_num

    return render_template("results.html", items_list=items, ids_list=response, page_id=1, page_num=page_num,
                           query_text=query_text, kw_text=keywords_text,
                           hits_num=len(response), start=1, DOC_PER_PAGE=DOC_PER_PAGE, option_analyzer=option_analyzer,
                           option_embed=option_embed,
                           contents=contents,
                           show_rel=SHOW_REL,
                           truncate_length=TRUNCATE_LENGTH,
                           )


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    items = [hit for hit in session["response"][(page_id - 1) * DOC_PER_PAGE: page_id * DOC_PER_PAGE]]
    contents = {hit.meta.id: hit.content for hit in
                session["response"][(page_id - 1) * DOC_PER_PAGE: page_id * DOC_PER_PAGE]}

    return render_template("results.html", items_list=items, ids_list=session["response"], page_id=page_id, page_num=session["page_num"],
                           query_text=session["query_text"], kw_text=session["keywords_text"], hits_num=len(session["response"]),
                           start=(page_id - 1) * DOC_PER_PAGE + 1,
                           DOC_PER_PAGE=DOC_PER_PAGE, option_analyzer=session["option_analyzer"], option_embed=session["option_embed"],
                           contents=contents,
                           show_rel=SHOW_REL,
                           truncate_length=TRUNCATE_LENGTH,
                           )


# document page
@app.route("/doc_data/<int:hit_idx>")
def doc_data(hit_idx):
    doc = session["response"][hit_idx]
    return render_template("doc.html", doc=doc)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

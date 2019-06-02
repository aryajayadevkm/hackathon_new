from flask import Flask, render_template, request, redirect, url_for, session
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
#from goodguide import page_soup, get_ingred_links, get_ingredients, get_rating, ingred_hazard, the_ingred_loop

app = Flask(__name__)
app.secret_key = "itsasecret"
@app.route('/', methods= ['GET','POST'])


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template("index.html")
    input = request.form['input']
    l = input.split(" ")
    input = "+".join(l)
    my_url = "https://www.goodguide.com/products?utf8=%E2%9C%93&filter=" + input + "&button=#/"
    session['my_url'] = my_url
    return redirect(url_for('product'))

@app.route('/product', methods=['GET','POST'])
def product():
    # calling the fn
    my_url = session.get('my_url')
    uClient = urlopen(my_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()

    # searching
    name = page_soup.find_all("span", {"class": "auto-truncated"})
    list_of_options = []
    try:
        for i in range(0, 8):
            list_of_options.append(name[i].text.strip())
    except:
        pass
    if request.method == 'GET':
        return render_template("details.html", list_of_options=list_of_options)
    elif request.method == 'POST':
        return render_template("details.html")
        product = request.form['product']
        print(product)


    productDivs = page_soup.find_all('div', {'class': 'large-2 columns text-center'})
    for div in productDivs:
        k = div.find('a')['title']
        if product.lower() == k.lower():
            session['link'] = div.find('a')['href']
            return redirect(url_for('/product/review'))
"""
@app.route("/product/review")
def product_review():
    link = session.get('link')
    page_soup(link)
"""



if __name__ == '__main__':
    app.run(port=5002)
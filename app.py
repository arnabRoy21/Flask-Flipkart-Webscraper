from flask import Flask, request, url_for, render_template, redirect
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        try:
            search_string = 'https://www.flipkart.com/search?q=' + request.form.get('product').replace(" ", '%20')

            product_page_html = requests.get(search_string).text
            product_page_html_parsed = BeautifulSoup(product_page_html, 'html.parser')
            
            product_item_search_string = product_page_html_parsed.find_all('div', attrs={'class' : '_1AtVbE col-12-12'})[4].div.div.div.a['href']
            
            product_item_search_string = 'https://www.flipkart.com' + product_item_search_string

            product_item_html = requests.get(product_item_search_string).text
            product_item_html_parsed = BeautifulSoup(product_item_html, 'html.parser')

            comment_boxes = product_item_html_parsed.find_all('div', attrs={'class' : 'col _2wzgFH'})

            data= []
            
            

            for comment_box in comment_boxes:
                comment_header = comment_box.div.p.text
                comment = comment_box.find_all('div', class_='')[1].text
                user = comment_box.find_all('p', class_='_2sc7ZR _2V5EHH')[0].text

                mydata = {
                    'user': user,
                    'comment_header': comment_header,
                    'comment': comment
                }

                data.append(mydata)
                # print(data)

        except:
            err_message = 'Something Went Wrong. Please try again'
            return render_template('index.html', err_message=err_message)
        
    return render_template('results.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
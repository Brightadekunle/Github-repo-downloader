import io
import pdfkit
import secrets
from io import BytesIO
from . import main
from App.scraper import GithubScrapper
from flask import Flask, render_template, session, redirect, url_for, send_file, request, make_response
from .form import DownloadForm


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('main.download'))

    return render_template('index.html')


@main.route('/download', methods=['GET', 'POST'])
def download():
    form = DownloadForm()
    crawler = GithubScrapper(session['username'], 2)
    df = crawler.getRepo()
    data = list(zip(df['Repo Name'].to_list(), df['url'].to_list()))

    if request.method == 'POST':
        towrite = io.BytesIO()
        df.to_excel(towrite)
        towrite.seek(0)
        return send_file(BytesIO(towrite.getvalue()), attachment_filename='Repo.xlsx', as_attachment=True)
    return render_template('download.html', data=data, form=form)


@main.route('/download-pdf', methods=['GET', 'POST'])
def download_pdf():
    form = DownloadForm()
    crawler = GithubScrapper(session['username'], 2)
    df = crawler.getRepo()
    data = list(zip(df['Repo Name'].to_list(), df['url'].to_list()))
    random = secrets.token_hex(8)

    if request.method == 'POST':
        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        rendered = render_template('pdf.html', data=data, form=form)
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['content-Type'] = "application/pdf"
        response.headers['content-Disposition'] = "attached: filename="+random+".pdf"
        return response

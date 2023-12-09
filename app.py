from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

ARCHIVE_COLLECTION = "YourCollection"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            item_title = request.form.get('title', 'UntitledItem')

            upload_to_archive(file_path, item_title)

            os.remove(file_path)  # Xóa tệp sau khi tải lên

            return render_template('success.html', archive_url=get_archive_url(item_title))

    return render_template('index.html')


def upload_to_archive(file_path, item_title):
    upload_url = "https://archive.org/serve/{}/{}".format(ARCHIVE_COLLECTION, item_title)

    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}
        data = {"name": file.name, "title": item_title, "description": "Uploaded via API"}
        response = requests.post(upload_url, files=files, data=data)

        if response.status_code != 200:
            print("Error uploading to Archive.org:", response.status_code)
            print("Response content:", response.text)


def get_archive_url(item_title):
    return "https://archive.org/details/{}".format(item_title)


if __name__ == '__main__':
    app.run(debug=True)

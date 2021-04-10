'''from django.views.generic import View, TemplateView, ListView, DetailView
from django.http import HttpResponse
from .models import Post
djangoのテンプレート
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from . import forms'''
import json
import subprocess
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from .application import item_research, user_research_20210404
from reportlab.pdfgen import canvas

#テンプレート呼び出し練習
'''class IndexView(TemplateView):
    template_name = "index.html"
    
    #HTMLに返却値を渡す
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["username"] = "Kei"
        return ctxt'''

#HTML以外の表示練習
body = """
<h1>Hello</h1>
<ol>
    <li>りんご</li>
    <li>ばなな</li>
    <li>いちご</li>
</ol>
"""

class IndexView(View):
    def get(self, request):
        return HttpResponse(body)

import csv

header = ['ID', '名前', '年齢']

people = [
    ('1', 'Hoge', 10),
    ('2', 'Fuga', 18),
    ('3', 'Foo', 23),
]

class CSVView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mycsv.csv"'
        
        writer = csv.writer(response)
        writer.writerow(header)
        writer.writerows(people)
        return(response)

import io

class PDFView(View):
    def get(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        
        #この部分を変えると内容が変わる
        p.drawString(50, 800, "Hello PDF!")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

class UserResearchView(View):
    
    def get(self, request):
        return render(request,"user_research.html")

    def post(self, request):
        print("ユーザー検索開始")
        category_url = request.POST['search_url']
        command = ["python3", "./brand_hunt/application/user_research.py", category_url]
        #user_json_data = user_research_20210404.get_user_research_json(category_url)
        #user_json_datas = json.loads(user_json_data)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        user_json_data = proc.stdout.read()
        #デコード
        dec_str_user_json_data = user_json_data.strip().decode('unicode-escape')
        #リプレイス
        rep_user_json_data = dec_str_user_json_data.replace('\"', '\'')
        #ダンプ
        dump_user_json_data = json.dumps(rep_user_json_data)
        user_json_datas = json.loads(dump_user_json_data)
        proc.communicate()
        print(user_json_datas)
        #return render(request,"user_research.html")
        return render(request,"user_research.html",{"user_json_datas":user_json_datas})

class ItemResearchView(View):
    
    def get(self, request):
        return render(request,"item_research.html")

    def post(self, request):
        salse_url = request.POST['search_url']
        item_json_data = item_research.get_item_research_json(salse_url)
        item_json_datas = json.loads(item_json_data)
        print(item_json_datas)
        return render(request,"item_research.html",{"item_json_datas":item_json_datas})

'''class AboutView(TemplateView):
    template_name = "about.html"
    
    #HTMLに返却値を渡す
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["num_service"] = 12345678
        ctxt["skills"] = [
            "Python",
            "Golang",
            "Java",
            "Swift",
        ]
        return ctxt

# ListViewは一覧を簡単に作るためのView
#class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
#    model = Post

# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post

# CreateViewは新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Post
    
    # 編集対象にするフィールド
    fields = ["title", "body", "category", "tags"]

class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]

class Delete(DeleteView):
    model = Post
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/"

class Index(FormView):
    form_class = forms.TextForm
    template_name = "brand_hunt/index.html"
    
    # フォームの入力にエラーが無かった場合に呼ばれます
    def form_valid(self, form):
        # form.cleaned_dataにフォームの入力内容が入っています
        data = form.cleaned_data
        text = data["text"]
        search = data["search"]
        replace = data["replace"]
        
        # ここで変換
        new_text = text.replace(search, replace)
        
        # テンプレートに渡す
        ctxt = self.get_context_data(new_text=new_text, form=form)
        return self.render_to_response(ctxt)'''
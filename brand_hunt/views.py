from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"
    
    #HTMLに返却値を渡す
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["username"] = "Kei"
        return ctxt
    
class AboutView(TemplateView):
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
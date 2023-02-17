from django import forms


class BootStrap:
    bootstrap_exclude_files = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_files:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         if field.widget.attrs:
    #             field.widget.attrs["class"] = "form-control"
    #             field.widget.attrs["placeholder"] = field.label
    #         else:
    #             field.widget.attrs = {
    #                 "class": "form-control",
    #                 "placeholder": field.label
    #             }


class BootStrapForm(BootStrap, forms.Form):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         if field.widget.attrs:
    #             field.widget.attrs["class"] = "form-control"
    #             field.widget.attrs["placeholder"] = field.label
    #         else:
    #             field.widget.attrs = {
    #                 "class": "form-control",
    #                 "placeholder": field.label
    #             }

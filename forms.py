from wtforms import Form, RadioField, StringField, TextAreaField


class ItemForm(Form):
    title = StringField('Title')
    description = StringField('Description')
    image = StringField('Image')
    content = TextAreaField ('Content')
    item_type = RadioField('Item type',  choices=[('thought', 'Thought'), ('project', 'Project')])
    publish = RadioField('Save or Publish', choices=[('save', 'Save'), ('publish', 'Publish')])

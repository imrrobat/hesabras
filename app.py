from nicegui import ui 
from utils import get_cat, add_cat
from snip import farsi_rtl, no_scroll

ui.add_head_html(no_scroll)
ui.add_head_html(farsi_rtl)

with ui.dialog().props('backdrop-filter="blur(8px) brightness(20%)"') as dialog, ui.card():
    ui.label('اضافه کردن دسته بندی')
    new_cat = ui.input('دسته بندی:')
    ui.button('اضافه کردن',on_click=lambda e:add_cat(new_cat.value))
    ui.button('بستن', on_click=dialog.close)

ui.button(icon='menu', on_click=dialog.open)

all_cats = get_cat()
for item in all_cats:
    ui.label(item)

ui.run()

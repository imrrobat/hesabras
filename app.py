from nicegui import ui 
from utils import get_cat, add_cat, add_income
from snip import farsi_rtl, no_scroll
import datetime 

ui.add_head_html(no_scroll)
ui.add_head_html(farsi_rtl)

def add_new_cat(e):
    add_cat(e)
    ui.notify('دسته بندی اضافه شد')
    dialog.close()
    cats.refresh()

def submit_income_or_expense():
    if ie_type.value=='دخل':
        if date.value:
            in_date = date.value
        else:
            today = datetime.datetime.today()
            in_date = f'{today.year}-{today.month:02d}-{today.day:02d}'
        add_income(
            title=ie_title.value or 'بدون تیتر',
            amount=ie_amount.value,
            category=ie_cat.value,
            income_date=in_date
        )
        ui.notify('اضافه شد')
    else:
        print('expense')

with ui.row().classes('w-full'):
    with ui.column().style('flex:1;border:solid 1px;'):
        with ui.row().classes('w-full p-2 m-2'):
            ie_title = ui.input('توضیحات').props('dense')
            ie_amount = ui.input('مقدار به تومان').props('dense')
            ie_type = ui.radio(['دخل','خرج'], value='خرج').props('dense')
        with ui.row().classes('w-full p-2'):
            ie_cat = None
            @ui.refreshable
            def cats():
                global ie_cat
                if ie_type.value == 'دخل':
                    all_cat = [k for k,v in get_cat().items() if v=='income']
                else:
                    all_cat = [k for k,v in get_cat().items() if v=='expense']
                print(get_cat())
                ie_cat = ui.select(options=all_cat, value=all_cat[-1]).props('dense').style('flex:4;')
            cats()
            with ui.dialog().props('backdrop-filter="blur(8px) brightness(20%)"') as dialog, ui.card():
                ui.label('اضافه کردن دسته بندی')
                new_cat = ui.input('دسته بندی:')
                with ui.row():
                    ui.button(icon='add',on_click=lambda e:add_new_cat(new_cat.value))
                    ui.button(icon='close', on_click=dialog.close)

            ui.button(icon='add', on_click=dialog.open).props('unelevated').style('flex:0.5;')
        with ui.row().classes('w-full p-2'):
            with ui.input('تاریخ').classes('w-full') as date:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date().bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button('Close', on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
        ui.button('ثبت', on_click=submit_income_or_expense).classes('w-full p-2')
                    
    with ui.column().style('flex:4;border:solid 1px;'):
        with ui.scroll_area():
            for i in range(50):
                ui.label(f'this is {i}')

ui.run()

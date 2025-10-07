from nicegui import ui 
from utils import get_cat, add_cat, add_data, read_data, aggregate_data
from snip import farsi_rtl, no_scroll
import datetime,jdatetime
import plotly.graph_objects as go


ui.add_head_html(no_scroll)
ui.add_head_html(farsi_rtl)

# ui.dark_mode(True)


def add_new_cat(e):
    typ = 'income' if new_typ.value=='درآمد' else 'expense'
    add_cat(e,typ=typ)
    ui.notify('دسته بندی اضافه شد')
    dialog.close()
    cats.refresh()

def submit_income_or_expense():
    if ie_amount.value:
        if date.value:
            in_date = date.value
        else:
            today = datetime.datetime.today()
            in_date = f'{today.year}-{today.month:02d}-{today.day:02d}'
        add_data(
            title=ie_title.value or 'بدون تیتر',
            amount=ie_amount.value,
            category=ie_cat.value,
            in_date=in_date,
            type='درآمد' if ie_type.value=='درآمد' else 'خرج'
        )
        ui.notify('اضافه شد')
        show_data.refresh()
    else:
        ui.notify('مقدار معتبر وارد کنید')

def show_jalali(e):
    if date.value:
        g_date = e.value  # مثلاً '2025-10-06'
        y, m, d = map(int, g_date.split('-'))
        j_date = jdatetime.date.fromgregorian(day=d, month=m, year=y)
        ui.notify(f'معادل شمسی: {j_date.strftime("%Y/%m/%d")}')

with ui.row().classes('w-full'):
    with ui.column().classes('items-center justify-center gap-1').style('flex:1;border:solid 1px;border-radius: 5px;'):
        with ui.row().classes('w-full p-2 m-2'):
              
            ie_amount = ui.input('مقدار به تومان')\
                .props('dense color=deep-purple mask="#,###,###,###" reverse-fill-mask input-class="text-left" required')
                
            ie_type = ui.radio(['درآمد','خرج'], value='خرج')\
                .props('dense color=deep-purple')
        with ui.row().classes('w-full p-2'):
            ie_cat = None
            @ui.refreshable
            def cats():
                global ie_cat
                if ie_type.value == 'درآمد':
                    all_cat = [item[0] for item in get_cat() if item[-1]=='income']
                else:
                    all_cat = [item[0] for item in get_cat() if item[-1]=='expense']
                ie_cat = ui.select(options=all_cat, value=all_cat[-1]).props('dense color=deep-purple').style('flex:4;')
            cats()
            ie_type.on_value_change(lambda e: cats.refresh())
            with ui.dialog().props('backdrop-filter="blur(8px) brightness(20%)"') as dialog, ui.card():
                with ui.row():
                    new_cat = ui.input('دسته بندی جدید:').props('dense').props('color=deep-purple')
                    new_typ = ui.radio(['درآمد','خرج'], value='درآمد').props('dense').props('color=deep-purple')
                with ui.row():
                    ui.button(icon='add',on_click=lambda e:add_new_cat(new_cat.value)).props('color=deep-purple')
                    ui.button(icon='close', on_click=dialog.close).props('color=deep-purple')

            ui.button(icon='add', on_click=dialog.open).props('unelevated').style('flex:0.5;').props('color=deep-purple')
        
        with ui.row().classes('w-full p-2'):
            with ui.input('تاریخ',placeholder='برای امروز خالی بگذارید').props('color=deep-purple').classes('w-full') as date:
                with ui.menu().props('color=deep-purple no-parent-event') as menu:
                    with ui.date(on_change=show_jalali).props('color=deep-purple').bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button('Close', on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            
        ie_title = ui.textarea('توضیحات')\
                .props('dense outlined color=deep-purple')\
                .classes('w-full')
        
        ui.button('ثبت', on_click=submit_income_or_expense)\
            .classes('w-full p-2')\
            .props('color=deep-purple')
            

        ui.link('آمار ماه جاری', 'http://127.0.0.1:8080/month', new_tab=True) \
            .classes('w-full p-2 q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-purple-5 text-white q-btn--actionable') \
            .style('border-radius:5px; display:flex; justify-content:center; align-items:center; text-decoration:none;')
            
                
                    
    with ui.column().style('flex:4;border:solid 1px;border-radius: 5px;height:700vh'):
        # with ui.scroll_area():
        #     for i in range(50):
        #         ui.label(f'this is {i}')
        @ui.refreshable
        def show_data():
            all_data = read_data()
            ui.aggrid({
                'columnDefs': [
                    {'headerName': 'زمان', 'field': 'date', 'width': 65,'filter': 'agTextColumnFilter', 'floatingFilter': True},
                    {'headerName': 'دسته بندی', 'field': 'category', 'width': 100},
                    {'headerName': 'مقدار', 'field': 'amount', 'width': 65,'filter': 'agNumberColumnFilter', 'floatingFilter': True},
                    {'headerName': 'توضیحات', 'field': 'title', 'width': 250,'filter': 'agTextColumnFilter', 'floatingFilter': True},
                    {
                        'headerName': 'نوع',
                        'field': 'type',
                        'width': 30,
                        'cellClassRules': {
                            'bg-red-300': 'x == "خرج"',
                            'bg-green-300': 'x == "درآمد"'
                        }
                    },
                ],
                'rowData': all_data,
            }).classes('h-full')
        show_data()
        
@ui.page('/month',title='آمار این ماه')    
def month():
    ui.add_head_html(farsi_rtl)
    ui.add_head_html(no_scroll)
    
    dt = datetime.datetime.today()
    this_month = f'{dt.year}-{dt.month:02d}'

    month_log = [item for item in read_data() if item['date'].startswith(this_month)]
    income_data = aggregate_data(month_log, 'درآمد')
    expense_data = aggregate_data(month_log, 'خرج')
    all_expense = sum(int(item['amount'].replace(',','')) for item in month_log)
    
    # ui.label(f'{all_expense:,}')
    
    def create_pie_chart(data_dict, title):
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        total = sum(values)
        
        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hoverinfo='label+percent+value',
                textinfo='label+percent',
                textfont_size=14
            )]
        )
        
        fig.update_layout(
            title=f"{title} - جمع کل: {total:,}",
            margin=dict(t=50, b=0, l=0, r=0)
        )
        
        return fig
    
    with ui.row().classes('w-full'):
        with ui.column().classes('items-center justify-center').style('flex:4;border:solid 1px;border-radius: 5px;'):
            ui.label('درآمدهای این ماه')
            ui.plotly(create_pie_chart(income_data, "درآمدها")).classes('w-1/2')
            
        with ui.column().classes('items-center justify-center').style('flex:4;border:solid 1px;border-radius: 5px;'):
            ui.label('مخارج این ماه')
            ui.plotly(create_pie_chart(expense_data, "خرج‌ها")).classes('w-1/2')
            
    
    

ui.run()

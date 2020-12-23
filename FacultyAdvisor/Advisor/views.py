from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import xlrd,os
from fpdf import FPDF
from django.http import FileResponse

import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
from .models import Sheet_model
def upload_sheet(request):
    return render(request,'upload_sheet.html')

def get_sheet(request):
    if request.method == 'POST':
        sheet = request.FILES.get('sheet')
        filename=request.FILES.get('sheet').name
        time_h=str(request.POST.get('time_h'))
        global date_h
        date_h=str(request.POST.get('date_h'))
        if sheet is None:
            return HttpResponse("File Not Found")
        else:
            print(time_h,date_h)
            Sheet_model.objects.filter(id=1).delete()
            file= Sheet_model(sheet=sheet)
            file.save()
            count = 0
            aval = []
            found=False
            x=os.path.join(BASE_DIR, 'media')+'/Sheets/'+filename
            wb = xlrd.open_workbook(x)
            sheet = wb.sheet_by_index(0)
            for i in range(3, sheet.ncols):
                if type(sheet.cell_value(3, i)) != str:
                    date1 = str(datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(3, i), 0)))[:10]
                    time1 = sheet.cell_value(4, i)
                    if date1 == date_h and time1 == time_h:
                        for j in range(5, sheet.nrows):
                            if sheet.cell_value(j, i) == 1:
                                aval.append(sheet.cell_value(j, 1))
                                found=True
                                count=count+1

            #creating text file
            d5='''Date: ''' + date_h
            x = os.path.join(BASE_DIR, 'media') + '/Sheets/text/demo.txt'
            s1 = ''
            s='''Shri Vaishnav Vidyapeeth Vishwavidyalaya
'''+'            '+sheet.cell_value(1,0 )+'''            
NOTICE
Time:'''+time_h+'\n'+d5+'\n'+'Available list of Faculties'+' ('+str(count)+')'
            f = open(x, "a")
            f1 = open(x, "w")
            f1.write('')
            f1.close()
            f.write(s)
            f.write('\n')
            j=1
            for i in aval:
                f.write('('+str(j)+') '+i)
                f.write('\n')
                j=j+1
            f.close()
            num=len(aval)
        parms={'list1':aval,'c':count,'date1':date_h,'time1':time_h,'found':found,'num':num}
        return render(request,'result.html',parms)
    else:
        return HttpResponse('Server Error')

def create_pdf(request):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    x = os.path.join(BASE_DIR, 'media') + '/Sheets/text/demo.txt'
    f = open(x, "r")

    a_file = open(x)
    lines_to_read = [0, 1, 2, 5]

    for position, line in enumerate(a_file):
        if position in lines_to_read:
            pdf.cell(0, 10, txt=line, ln=2, align='C')
        else:
            pdf.cell(300, 10, txt=line, ln=2, align='L')
    x = os.path.join(BASE_DIR, 'media') + '/Sheets/pdf/'+'report'+date_h+'.pdf'
    pdf.output(x)
    a_file.close()
    f.close()


    pdf1 = open(x, 'rb')
    response = FileResponse(pdf1)
    return response
from django.db import connection

def run_raw_proc(proc_statement, *proc_args):
    cursor =  connection.cursor().execute(proc_statement, *proc_args)
<<<<<<< HEAD
    resultarr = []
    while True:
        if cursor.description != None:
            columns = [col[0] for col in cursor.description]
            dictset = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
            if len(dictset) > 0: resultarr.append(dictset)
        if not cursor.nextset(): break
    return resultarr
=======
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]
>>>>>>> upstream/develop

def get_invoice_report_data(invoiceId):
    return run_raw_proc("EXEC dbo.UP_S_GetInvoiceReport @InvoiceId = '{}';".format(invoiceId))

# def get_invoice_detail_data(invoiceId):
#     return run_raw_proc("EXEC dbo.UP_S_GetInvoiceReport @InvoiceId = '{}';".format(invoiceId))
import React, { useState } from 'react';
import InvoiceListMain from '../components/InvoiceListMain';
import InvoiceListDetail from '../components/InvoiceListDetail';

function GridPage() {
    const [invoiceId, setInvoiceId] = useState(0)

    return (
        <>
            <InvoiceListMain setInvoiceId={setInvoiceId} />
            <InvoiceListDetail invoiceId={invoiceId} />
        </>
    )
}

export default GridPage;

import React, { useState } from 'react';
import MainGrid from './MainGrid';
import DetailGrid from './DetailGrid';

function GridPage() {
    const [invoiceId, setInvoiceId] = useState(0)

    return (
        <>
            <MainGrid setInvoiceId={setInvoiceId} />
            <DetailGrid invoiceId={invoiceId} />
        </>
    )
}

export default GridPage;

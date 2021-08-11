import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PDFViewer } from '@react-pdf/renderer';
import DocPDF from './DocPDF2';
import ErrorMsg from './ErrorMsg';

function ReportApp({ data }) {
    return (
        <PDFViewer frameBorder={0} style={{position: 'fixed', top: 0, left: 0, height: '100%', width: '100%', margin: 0}}>
            <DocPDF data={data} />
        </PDFViewer>
    )
}

function ReportLoading() {
    return (
        <>
            로딩중...!
        </>
    )
}

function Report({ match }) {
    const [data ,setData] = useState(null)
    const [err, setErr] = useState(null)
    const id = match.params.id;
    const url = `/api/v1/invoice_report/${id}`

    useEffect(()=>{
        axios.get(url)
            .then((res) => {
                setData(res.data)
            })
            .catch((err) => {
                console.log(err.response)
                setErr(err.response.status)
            })
    },[])

    if (err) {
        return <ErrorMsg status={err} />
    }

    if (data) {
        return <ReportApp data={data} />
    } else {
        return <ReportLoading />
    }
}

export default Report
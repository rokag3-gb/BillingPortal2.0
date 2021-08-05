import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PDFViewer } from '@react-pdf/renderer';
import DocPDF from './DocPDF2';

function Report({ match }) {
    const [data ,setData] = useState(null)
    const id = match.params.id;
    const url = `/api/v1/invoice_report/${id}`

    useEffect(()=>{
        axios.get(url)
            .then((res) => {
                setData(res.data)
            })
            .catch((err) => {
                console.log(err.response)
            })
    },[])
    
    return (
        <>
            <PDFViewer frameBorder={0} style={{position: 'fixed', top: 0, left: 0, height: '100%', width: '100%', margin: 0}}>
                {data && <DocPDF data={data} />}
            </PDFViewer>
        </>
    )
}

export default Report
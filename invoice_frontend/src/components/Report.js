import React, { useState } from 'react'
import { PDFViewer } from '@react-pdf/renderer';

import DocPDF from './DocPDF'

const clientInfo = {
    name: "주식회사 어디",
    manager: "정떙땡그룹장님",
    call: "010-1111-2222",
    mail: "dummy123@dummy.com",
}
const paymentInfo = {
    payment: ["card", "cash"],
    paymentYear: 2021,
    paymentMonth: 7,
    period: ["2021-07-01", "2021-07-31"],
    paymentCondition: "Net 30", // ??
}
const cloudServiceUsageInfo = [
    { supplier: "Microsoft", service: "Azure", serviceName: "EC2다", quantity: 12, price: 500000, total: 6000000 },
    { supplier: "AWS", service: "M365", serviceName: "E5 Plan", quantity: 12, price: 2000000, total: 24000000 },
]
const additionalServiceUsageInfo = [
    { supplier: "Cloudmate", service: "시스템 현황 분석 및 기능설정", serviceName: "시스템 환경 분석 및 요구사항 정의", quantity: 0.2, price: 1000000, total: 200000 },
    { supplier: "Cloudmate", service: "운영", serviceName: "운영", quantity: 1, price: 1000000, total: 1000000 },
]

function Report({ match }) {
    const id = match.params.id;

    useState(()=>{
        // TODO: load invoice info
    },[])

    return (
        <>
            <PDFViewer frameBorder={0} style={{position: 'fixed', top: 0, left: 0, height: '100%', width: '100%', margin: 0}}>
                <DocPDF
                    id={id}
                    clientInfo={clientInfo}
                    paymentInfo={paymentInfo}
                    cloudServiceUsageInfo={cloudServiceUsageInfo}
                    additionalServiceUsageInfo={additionalServiceUsageInfo}
                />
            </PDFViewer>
        </>
    )
}

export default Report
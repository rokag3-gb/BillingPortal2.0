import React from 'react'
import { Page, Text, View, Document, StyleSheet, Font, Image } from '@react-pdf/renderer';

import font from '../assets/malgun.ttf'
import fontBd from '../assets/malgunbd.ttf'
import logo from '../assets/logo.png'
import { COMPANY, ADDRESS, EMAIL, CALL_LOCAL, URL_APP, URL_HOME, REMARKS } from '../config'
import TablePDF from './TablePDF';

const styles = StyleSheet.create({
    page: {
        // flexDirection: 'column',
        padding: 20,
        fontFamily: 'malgun',
        fontSize: '8px',
        lineHeight: '1.6',
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingBottom: 3,
        borderBottomColor: 'grey',
        borderBottomWidth: 1,
    },
    headerLogo: {
        width: 132,
        height: 33
    },
    headerMain: {
        flexGrow: 1,
        marginLeft: 10
    },
    headerSub: {
        alignItems:"flex-end"
    },
    textTitle: {
        fontSize: '12px',
        fontWeight: 'bold'
    },
    textSubTitle: {
        fontSize: '11px',
        fontWeight: 'bold',
    },
    textHeader: {
        fontSize: '10px',
        fontWeight: 'bold',
        borderBottomColor: 'grey',
        borderBottomWidth: 1,
        borderStyle: 'dashed',
    },
    textInvoiceID: {
        fontSize: '9px',
        fontWeight: 'bold',
        color: 'red',
    },
    sectionTitle: {
        marginVertical: 10,
    },
    sectionSummary: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    sectionDetail: {
        marginTop: 10,
    },
    detailTitle: {
        fontSize: '9px',
        fontWeight: 'bold',
        backgroundColor: '#e4e4e4',
        marginTop: 10,
    },
    sectionTotal: {
        flexDirection: 'row-reverse',
        marginTop: 10,
    },
    sectionRemark: {

    },
})

function DocPDF({ id, clientInfo, paymentInfo, cloudServiceUsageInfo, additionalServiceUsageInfo }) {
    const usagePeriod = `${paymentInfo.period[0]} ~ ${paymentInfo.period[1]}`
    const payYear = paymentInfo.paymentYear
    const payMonth = paymentInfo.paymentMonth
    const sumCloud = cloudServiceUsageInfo.reduce((prv, cur) => prv + cur.total, 0)
    const sumAdditional = additionalServiceUsageInfo.reduce((prv, cur) => prv + cur.total, 0)
    const supply = sumCloud + sumAdditional
    const vat = supply * 0.1
    const total = supply + vat
    const detailTableColumns = ["No.", "Supplier", "Service", "Service Name", "Q`ty", "Unit Price", "Total"]
    const detailTableSize = [20,70,100,0,30,70,70]//40
    const cloudServiceRows = cloudServiceUsageInfo.map((item, idx) => 
        [idx + 1, item.supplier, item.service, item.serviceName, item.quantity, item.price, item.total]
    )
    const additionalServiceRows = additionalServiceUsageInfo.map((item, idx) =>
        [idx + 1, item.supplier, item.service, item.serviceName, item.quantity, item.price, item.total]
    )    

    Font.register({
        family: 'malgun',
        fonts: [
            { src: font },
            { src: fontBd, fontWeight: 600}
        ]
    })
    
    return (
        <Document>
            <Page size='A4' style={styles.page}>
                <View style={styles.sectionHeader}>
                    <View>
                        <Image style={styles.headerLogo} src={logo} />
                    </View>
                    <View style={styles.headerMain}>
                        <Text style={styles.textTitle}>
                            {COMPANY}
                        </Text>
                        <Text>{ADDRESS} / {CALL_LOCAL} / {EMAIL}</Text>
                    </View>
                    <View style={styles.headerSub}>
                        <Text>{URL_APP}</Text>
                        <Text>{URL_HOME}</Text>
                        <Text style={styles.textInvoiceID}>
                            Invoice No: {id}
                        </Text>
                    </View>
                </View>
                <View style={styles.sectionTitle}>
                    <Text style={styles.textSubTitle}>
                        {payYear}년 {payMonth}월 분 청구서
                    </Text>
                </View>
                <View style={styles.sectionSummary}>
                    <View>
                        <Text style={styles.textHeader}>계약고객정보</Text>
                        <TablePDF
                            // columns={["col_1", "col_2"]}
                            size={[80, 150]}
                            rows={[
                                ["기업명", clientInfo.name],
                                ["담당자", clientInfo.manager],
                                ["연락처", clientInfo.call],
                                ["이메일", clientInfo.mail],
                            ]}
                        />
                        <Text style={{fontWeight: 'bold', paddingTop: '5px'}}>청구정보</Text>
                        <TablePDF
                            size={[80, 150]}
                            rows={[
                                ["사용기간", usagePeriod],
                                ["결제방법", paymentInfo.payment[0]],
                                ["결제조건", paymentInfo.paymentCondition]
                            ]}
                        />
                    </View>
                    <View>
                        <Text style={styles.textHeader}>청구정보 요약</Text>
                        <Text style={{fontWeight: 'bold', paddingTop: '5px'}}>청구항목</Text>
                        <TablePDF
                            size={[120, 180]}
                            rows={[
                                [`${payYear}년 ${payMonth}월 분 청구금액`, total],
                                ["CSP서비스(1번항목)", sumCloud],
                                ["부가서비스(2번항목)", sumAdditional],
                                ["공급금액", supply],
                                ["부가가치세", vat]
                            ]}
                            border
                            boldText
                        />
                    </View>
                </View>
                <View style={styles.sectionDetail}>
                    <Text style={styles.textHeader}>청구상세내역</Text>
                    <Text style={styles.detailTitle}>1. Cloud Services / Appliance</Text>
                    <TablePDF
                        columns={detailTableColumns}
                        size={detailTableSize}
                        rows={cloudServiceRows}
                    />
                    <Text style={styles.detailTitle}>2. Additional Services</Text>
                    <TablePDF
                        columns={detailTableColumns}
                        size={detailTableSize}
                        rows={additionalServiceRows}
                    />
                </View>
                <View style={styles.sectionTotal}>
                    <TablePDF
                        size={[110, 100]}
                        rows={[
                            ["공급가액 (부가가치세 별도)", supply],
                            ["부가가치세 (10%)", vat],
                            ["합 계 액", total]
                        ]}
                        border
                        boldText
                    />
                </View>
                <View style={styles.sectionRemark}>
                    <Text style={styles.textHeader}>Remarks</Text>
                    {REMARKS.map((text, idx) => <Text key={'rm'+idx} style={{marginLeft: 5}}>{`${idx+1}. ${text}`}</Text>)}
                </View>
            </Page>
        </Document>
    )
}

export default DocPDF
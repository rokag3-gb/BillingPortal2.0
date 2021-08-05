import React from 'react'
import { Page, Text, View, Document, StyleSheet, Font, Image } from '@react-pdf/renderer';
import font from '../assets/malgun.ttf';
import fontBd from '../assets/malgunbd.ttf';
import logo from '../assets/logo.png';
import { URL_APP, URL_HOME } from '../config';
import TablePDF from './TablePDF';
import * as utils from '../utils';

const styles = StyleSheet.create({
    page: {
        paddingLeft: 20,
        paddingRight: 20,
        paddingTop: 20,
        paddingBottom: 40,
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
    pageNumber: {
        position: 'absolute',
        bottom: 20,
        left: 0,
        right: 0,
        textAlign: 'center',
    },
    printTime: {
        position: 'absolute',
        bottom: 30,
        left: 0,
        right: 20,
        textAlign: 'right',
    }
})
const nullMsg = (t) => t ? t : "없음"
const AdditionalTable = ({columns, size, rows}) => {
    return (
        <>
            <Text style={styles.detailTitle}>2. Additional Services</Text>
            <TablePDF
                columns={columns}
                size={size}
                rows={rows}
            />
        </>
    )
}

function DocPDF({ data }) {
    const detailTableColumns = ["No.", "Supplier", "Service", "Service Name", "Q`ty", "Unit Price", "Total"]
    const detailTableSize = [20,70,100,200,30,70,70]//40
    const commonData = data[0][0]
    const summaryRows = data[1].sort((a, b) => a.sort - b.sort).map((item) => [item.itemName, item.amount])
    const cloudServiceRows = data[2].map((item, idx) =>
        [idx +1, item.supplier, item.service, item.serviceName, item.quantity, item.price, item.amount]
    )
    let additional = false
    let additionalServiceRows = null
    let totalData = data[3]

    const now = new Date()
    const date = utils.getDateFormat(now)
    const times = utils.getTimeFormat(now)

    if (data.length === 5) {
        // Additional 서비스 있음
        additional = true
        additionalServiceRows = data[3].map((item, idx) =>
            [idx +1, item.supplier, item.service, item.serviceName, item.quantity, item.price, item.amount]
        )
        totalData = data[4]
    }

    const totalRows = totalData.sort((a, b) => a.sort - b.sort).map((item) => [item.itemName, item.amount])

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
                            {commonData.ProviderName}
                        </Text>
                        <Text>{commonData.ProviderAddress}</Text>
                    </View>
                    <View style={styles.headerSub}>
                        <Text>{URL_APP}</Text>
                        <Text>{URL_HOME}</Text>
                        <Text style={styles.textInvoiceID}>
                            Invoice No: {commonData.InvoiceId}
                        </Text>
                    </View>
                </View>
                <View style={styles.sectionTitle}>
                    <Text style={styles.textSubTitle}>
                        {commonData.InvoiceTitle}
                    </Text>
                </View>
                <View style={styles.sectionSummary}>
                    <View>
                        <Text style={styles.textHeader}>계약고객정보</Text>
                        <TablePDF
                            // columns={["col_1", "col_2"]}
                            size={[80, 150]}
                            rows={[
                                ["기업명", commonData.OrgName],
                                ["담당자", nullMsg(commonData.UserName)],
                                ["연락처", nullMsg(commonData.UserPhone)],
                                ["이메일", nullMsg(commonData.UserEmail)],
                            ]}
                        />
                        <Text style={{fontWeight: 'bold', paddingTop: '5px'}}>청구정보</Text>
                        <TablePDF
                            size={[80, 150]}
                            rows={[
                                ["사용기간", commonData.ChargePeriod],
                                ["결제방법", commonData.PaymentMethod],
                                ["결제조건", commonData.PaymentCondition]
                            ]}
                        />
                    </View>
                    <View>
                        <Text style={styles.textHeader}>청구정보 요약</Text>
                        <Text style={{fontWeight: 'bold', paddingTop: '5px'}}>청구항목</Text>
                        <TablePDF
                            size={[120, 180]}
                            rows={summaryRows}
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
                    {additional && <AdditionalTable columns={detailTableColumns} size={detailTableSize} rows={additionalServiceRows} />}
                </View>
                <View style={styles.sectionTotal}>
                    <TablePDF
                        size={[110, 100]}
                        rows={totalRows}
                        border
                        boldText
                    />
                </View>
                <View style={styles.sectionRemark}>
                    <Text style={styles.textHeader}>Remarks</Text>
                    <Text style={{marginLeft: 5}}>
                        {commonData.Remark}
                    </Text>
                </View>
                <Text style={styles.printTime} fixed>Document printing time: {`${date} ${times}`}</Text>
                <Text
                    style={styles.pageNumber}
                    render={({ pageNumber, totalPages }) => (
                        `Page ${pageNumber} of ${totalPages}`
                    )}
                    fixed
                />
            </Page>
        </Document>
    )
}

export default DocPDF
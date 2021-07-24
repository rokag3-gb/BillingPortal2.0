import React from 'react';
import DataGrid, {
    Button,
    Column,
    ColumnChooser,
    FilterRow,
    Scrolling,
} from 'devextreme-react/data-grid';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';

const urlInvoice = "/api/v1/invoice/"
const headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json'
}

const store = new CustomStore({
    key: 'seq',
    load: function() {
        const url = urlInvoice + "?limit=1000"

        return axios.get(url)
            .then((res) => {
                console.log(`GET ${url} ok - len:${res.data.results.length}`)
                
                return res.data.results
            })
            .catch((err) => {
                console.log(`GET ${url} fail`)
                throw new Error("데이터 불러오기 실패")
            })
    },
    insert: function(values) {
        return axios.post(urlInvoice, values, { headers })
            .then((res) => {
                console.log(`POST ${urlInvoice} ok`)
            })
            .catch((err) => {
                console.log(err.response.data)
                throw new Error("데이터 생성 실패")
            })
    },
    update: function(key, values) {
        const url = urlInvoice + key

        return axios.put(url, values, { headers })
            .then((res) => {
                console.log(`PUT ${url} ok`)
            })
            .catch((err) => {
                console.log(err.response)
                throw new Error(`데이터 업데이트 실패(Seq: ${key})`)
            })
    },
    remove: function(key) {
        const url = urlInvoice + key

        return axios.delete(url, { headers })
            .then((res) => {
                console.log(`DELETE ${url} ok`)
            })
            .catch((err) => {
                console.log(err.response)
                throw new Error(`데이터 삭제 실패(Seq: ${key})`)
            })
    }
});

const ds = new DataSource({
    store: store
})

function MainGrid({ setInvoiceId }) {
    const handlePDF = (e) => {
        e.event.preventDefault()
        window.open(`report/${e.row.data.invoiceId}`, "_blank")
        // New window
        // window.open(`report/${e.row.data.invoiceId}`, "_blank", "resizable, width=650, height=950")
    }
    const handleDetail = (e) => {
        e.event.preventDefault()
        setInvoiceId(e.row.data.invoiceId)
    }

    return (
        <>
            <DataGrid
                dataSource={ds}
                showBorders
                columnAutoWidth
                style={{height: '45vh'}}
            >
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Scrolling mode="virtual" />

                <Column type="buttons" width="80">
                    <Button icon="pdffile" onClick={handlePDF} />
                    <Button icon="showpanel" onClick={handleDetail} />
                </Column>
                <Column dataField="seq" />
                <Column dataField="invoiceMonth" />
                <Column dataField="invoiceDate" />
                <Column dataField="invoiceId" />
                <Column dataField="orgId" />
                <Column dataField="orgKey"visible={false} />
                <Column dataField="orgName" />
                <Column dataField="vendorCode"visible={false} />
                <Column dataField="vendorName"visible={false} />
                <Column dataField="vendorInvoiceCount"visible={false} />
                <Column dataField="chargeStartDate" />
                <Column dataField="chargeEndDate" />
                <Column dataField="partner_amount_pretax" visible={true} />
                <Column dataField="rrp_amount_pretax" />
                <Column dataField="our_amount_pretax" />
                <Column dataField="our_tax" />
                <Column dataField="our_amount" />
                <Column dataField="paid" />
                <Column dataField="regId" />
                <Column dataField="regDate" />
                <Column dataField="stateCode" />
                <Column dataField="stateChgId" />
                <Column dataField="stateChgDate"/ >
                <Column dataField="remark" />

            </DataGrid>
        </>
    );
}

export default MainGrid;
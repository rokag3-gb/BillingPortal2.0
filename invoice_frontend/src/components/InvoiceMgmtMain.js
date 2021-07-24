import React from 'react';
import DataGrid, {
    Button,
    Column,
    Editing,
    RequiredRule,
    ColumnChooser,
    FilterRow,
    Pager,
    Paging,
    PatternRule,
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
        // window.open(`report/${e.row.data.invoiceId}`, "_blank", "resizable, width=650, height=950")
        window.open(`report/${e.row.data.invoiceId}`, "_blank")
    }
    const handleRowUpdating = (e) => {
        e.newData = {...e.oldData, ...e.newData}
    }
    const handleDetail = (e) => {
        e.event.preventDefault()
        // setDetailOrgId(e.row.data.orgId)
        setInvoiceId(e.row.data.invoiceId)
    }

    return (
        <>
            MgmtMain
            <DataGrid
                dataSource={ds}
                showBorders
                columnAutoWidth
                onRowUpdating={handleRowUpdating}
            >
                <Editing
                    mode="batch"
                    allowAdding
                    allowDeleting
                    allowUpdating
                    startEditAction="dblClick"
                />
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Paging defaultPageSize={10} />
                <Pager
                    visible={true}
                    allowedPageSizes={[5, 10, 15, 20]}
                    showPageSizeSelector={true}
                    showInfo={true}
                    showNavigationButtons={true}
                />

                <Column type="buttons" width="90">
                    <Button icon="pdffile" onClick={handlePDF} />
                    <Button icon="showpanel" onClick={handleDetail} />
                    <Button name="delete" />
                </Column>
                {/* <Column type="buttons" width="70" /> */}

                <Column dataField="seq" allowEditting={false} />
                <Column dataField="invoiceMonth" allowEditting={false}>
                    <RequiredRule />
                </Column>
                <Column dataField="invoiceDate" allowEditting={true}>
                    <RequiredRule />
                </Column>
                <Column dataField="invoiceId" allowEditting={false} />
                <Column dataField="orgId" allowEditting={false}>
                    <RequiredRule />
                </Column>
                <Column dataField="orgKey" allowEditting={false} visible={false} />
                <Column dataField="orgName" allowEditting={true} />
                <Column dataField="vendorCode" allowEditting={false} visible={false} />
                <Column dataField="vendorName" allowEditting={false} visible={false} />
                <Column dataField="vendorInvoiceCount" allowEditting={false} visible={false} />
                <Column dataField="chargeStartDate" allowEditting={true}>
                    <RequiredRule />
                </Column>
                <Column dataField="chargeEndDate" allowEditting={true}>
                    <RequiredRule />
                </Column>
                <Column dataField="partner_amount_pretax" allowEditting={false} visible={true} />
                <Column dataField="rrp_amount_pretax" allowEditting={false} />
                <Column dataField="our_amount_pretax" allowEditting={false} />
                <Column dataField="our_tax" allowEditting={false} />
                <Column dataField="our_amount" allowEditting={false} />
                <Column dataField="paid" allowEditting={false} />
                <Column dataField="regId" allowEditting={false}>
                    <RequiredRule />
                </Column>
                <Column dataField="regDate" allowEditting={false} />
                <Column dataField="stateCode" allowEditting={true}>
                    <RequiredRule />
                </Column>
                <Column dataField="stateChgId" allowEditting={false} />
                <Column dataField="stateChgDate" allowEditting={false} />
                <Column dataField="remark" allowEditting={true} />

            </DataGrid>
        </>
    );
}

export default MainGrid;
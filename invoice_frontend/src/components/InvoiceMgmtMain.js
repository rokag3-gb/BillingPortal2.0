import React, { useRef } from 'react';
import DataGrid, {
    Button as CellButton,
    Column,
    ColumnChooser,
    FilterRow,
    Selection,
    Summary,
    TotalItem,
    Format,
    Editing,
    RequiredRule,
    Paging,
} from 'devextreme-react/data-grid';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';

const url = "/api/v1/invoice/"
const headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json'
}

function loadStore(loadOptions, param) {
    console.log("load main store")
    return axios.get(url + param)
        .then((res) => {
            console.log(`GET ${url + param} ok - len:${res.data.results.length}`)
            return res.data.results.map((data) => (
                {
                    ...data,
                    partner_amount_pretax: parseFloat(data.partner_amount_pretax),
                    rrp_amount_pretax: parseFloat(data.rrp_amount_pretax),
                    our_amount_pretax: parseFloat(data.our_amount_pretax),
                    our_tax: parseFloat(data.our_tax),
                    our_amount: parseFloat(data.our_amount),
                    paid: parseFloat(data.paid)
                }
            ))
        })
        .catch((err) => {
            console.log(`GET ${url} fail`)
            console.log(err.response)
            throw new Error("데이터 불러오기 실패")
        })
}
function insertStore(values) {
    return axios.post(url, values, { headers })
        .then((res) => {
            console.log(`POST ${url} ok`)
        })
        .catch((err) => {
            console.log(err.response.data)
            throw new Error("데이터 생성 실패")
        })
}
function updateStore(key, values) {
    return axios.put(url + key, values, { headers })
        .then((res) => {
            console.log(`PUT ${url} ok`)
        })
        .catch((err) => {
            console.log(err.response)
            throw new Error(`데이터 업데이트 실패(Seq: ${key})`)
        })    
}
function removeStore(key) {
    return axios.delete(url + key, { headers })
        .then((res) => {
            console.log(`DELETE ${url} ok`)
        })
        .catch((err) => {
            console.log(err.response)
            throw new Error(`데이터 삭제 실패(Seq: ${key})`)
        })
}
const getInvoiceIds = (rowsData) => rowsData.map((row) => row.invoiceId)

function InvoiceMgmtMain({ param, setInvoiceId }) {
    const storeMain = new CustomStore({
        key: 'seq',
        load: (loadOptions) => param ? loadStore(loadOptions, param) : null,
        insert: insertStore,
        update: updateStore,
        remove: removeStore
    });
    const dsMain = new DataSource({store: storeMain})
    const refDataGrid = useRef(null);
    const handlePDFClick = (e) => {
        e.event.preventDefault()
        window.open(`report/${e.row.data.invoiceId}`, "_blank")
    }
    const handleDetailClick = (e) => {
        e.event.preventDefault()
        setInvoiceId(e.row.data.invoiceId)
    }
    const handlePaymentClick = () => {
        if (refDataGrid === null) { return }
        const dg = refDataGrid.current.instance;
        const selectedInvoiceIds = getInvoiceIds(dg.getSelectedRowsData())
        if (selectedInvoiceIds.length) {
            window.parent.proceed_payment(selectedInvoiceIds)
        }
    }
    const handleToolbarPreparing = (e) => {
        e.toolbarOptions.items.unshift(
            {
                location: 'after',
                widget: 'dxButton',
                options: {
                    text: '결제하기',
                    onClick: handlePaymentClick
                }
            },
        )
    }
    const calculateCustomSummary = (options) => {
        if (options.name === "UniqueOrg") {
            if (options.summaryProcess === "start") {
                options.totalValue = []
            }
            if (options.summaryProcess === "calculate") {
                if (!options.totalValue.includes(options.value.orgId)) {
                    options.totalValue.push(options.value.orgId)
                }
            }
            if (options.summaryProcess === "finalize") {
                options.totalValue = "Count: " + options.totalValue.length
            }
        }
    }
    const indexRender = (a) => typeof a.row.dataIndex === 'number' ? <div style={{textAlign: 'center'}}>{a.row.dataIndex+1}</div> : null;
    const handleRowUpdating = (e) => {
        e.newData = {...e.oldData, ...e.newData}
    }
    return (
        <div>
            <DataGrid
                dataSource={dsMain}
                showBorders
                columnAutoWidth
                style={{height: '45vh'}}
                hoverStateEnabled={true}
                ref={refDataGrid}
                onToolbarPreparing={handleToolbarPreparing}
                allowColumnResizing={true}
                columnResizingMode="widget"
                showRowLines
                rowAlternationEnabled
                onRowUpdating={handleRowUpdating}
            >
                <Editing
                    mode="batch"
                    allowAdding
                    allowDeleting
                    allowUpdating
                    startEditAction="dblClick"
                    useIcons
                />
                <Selection mode="multiple" />
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Paging enabled={false} />

                <Column type="buttons" width="95">
                    <CellButton icon="pdffile" onClick={handlePDFClick} text="리포트" />
                    <CellButton icon="showpanel" onClick={handleDetailClick} text="상세보기" />
                    <CellButton name="delete" />
                </Column>
                <Column caption="#" cellRender={indexRender} />
                <Column dataField="seq" />
                <Column dataField="invoiceMonth">
                    <RequiredRule />
                </Column>
                <Column dataField="invoiceDate" dataType="date" format="yyyy-MM-dd">
                    <RequiredRule />
                </Column>
                <Column dataField="invoiceId" />
                <Column dataField="orgId">
                    <RequiredRule />
                </Column>
                <Column dataField="orgKey"visible={false} />
                <Column dataField="orgName" />
                <Column dataField="vendorCode"visible={false} />
                <Column dataField="vendorName"visible={false} />
                <Column dataField="vendorInvoiceCount"visible={false} />
                <Column dataField="chargeStartDate" dataType="date" format="yyyy-MM-dd">
                    <RequiredRule />
                </Column>
                <Column dataField="chargeEndDate" dataType="date" format="yyyy-MM-dd">
                    <RequiredRule />
                </Column>
                <Column dataField="partner_amount_pretax" caption="partner_amount" visible={true}>
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="rrp_amount_pretax" caption="rrp_amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_amount_pretax" caption="amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_tax" caption="tax">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_amount" caption="amount + tax">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="paid">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="regId">
                    <RequiredRule />
                </Column>
                <Column dataField="regDate" />
                <Column dataField="stateCode" />
                <Column dataField="stateChgId" />
                <Column dataField="stateChgDate"/ >
                <Column dataField="remark" />
                <Summary calculateCustomSummary={calculateCustomSummary}>
                    <TotalItem column="seq" summaryType="count" valueFormat=",##0" />
                    <TotalItem
                        name="UniqueOrg"
                        summaryType="custom"
                        showInColumn="orgId"
                    />
                    <TotalItem column="partner_amount_pretax" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="rrp_amount_pretax" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="our_amount_pretax" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="our_tax" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="our_amount" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="paid" summaryType="sum" valueFormat=",##0" />
                </Summary>
            </DataGrid>
        </div>
    );
}

export default React.memo(InvoiceMgmtMain);
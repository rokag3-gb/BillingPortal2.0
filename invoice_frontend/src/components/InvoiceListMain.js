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
    Paging,
} from 'devextreme-react/data-grid';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';

const url = "/api/v1/invoice/"
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
            if (err.response.data) {
                let msg = ""
                for (const [key, value] of Object.entries(err.response.data)) {
                    msg += `${key}: ${value} `
                }
                throw new Error(msg)
            }
            throw new Error("데이터 불러오기 실패")
        })
}
const getInvoiceIds = (rowsData) => rowsData.map((row) => row.invoiceId)

function InvoiceListMain({ param, setInvoiceId }) {
    const storeMain = new CustomStore({
        key: 'seq',
        load: (loadOptions) => param ? loadStore(loadOptions, param) : null
    });
    const dsMain = new DataSource({store: storeMain})
    const refDataGrid = useRef(null);
    const handlePDFClick = (e) => {
        e.event.preventDefault()
        window.open(`../report/${e.row.data.invoiceId}`, "_blank")
    }
    const handleDetailClick = (e) => {
        e.event.preventDefault()
        setInvoiceId(e.row.data.invoiceId)
    }
    const handleDbClick = (e) => {
        e.event.preventDefault()
        setInvoiceId(e.data.invoiceId)
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
                    text: '결제',
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
    const indexRender = (a) => (<div style={{textAlign: 'center'}}>{a.row.dataIndex+1}</div>)
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
                onRowDblClick={handleDbClick}
            >
                <Selection mode="multiple" />
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Paging enabled={false} />

                <Column type="buttons" width="80" allowHiding={false} fixed fixedPosition='left' allowResizing={false}>
                    <CellButton icon="pdffile" onClick={handlePDFClick} text="리포트" />
                    <CellButton icon="showpanel" onClick={handleDetailClick} text="상세보기" />
                </Column>
                <Column caption="#" cellRender={indexRender} allowHiding={false} fixed={true} />
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
                <Column dataField="regId" />
                <Column dataField="regDate" dataType="date" format="yyyy-MM-dd HH:mm:ss" />
                <Column dataField="stateCode" />
                <Column dataField="stateChgId" />
                <Column dataField="stateChgDate" dataType="date" format="yyyy-MM-dd HH:mm:ss" />
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

export default React.memo(InvoiceListMain);
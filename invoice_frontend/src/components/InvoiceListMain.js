import React, { useRef } from 'react';
import DataGrid, {
    Button as CellButton,
    Column,
    ColumnChooser,
    FilterRow,
    Scrolling,
    Selection,
    Summary,
    TotalItem,
    Format,
    Editing,
} from 'devextreme-react/data-grid';

const getInvoiceIds = (rowsData) => rowsData.map((row) => row.invoiceId)
function MainGrid({ ds, setInvoiceId, setStartDate, getStartDate }) {
    const refDataGrid = useRef(null);
    const handlePDFClick = (e) => {
        e.event.preventDefault()
        window.open(`report/${e.row.data.invoiceId}`, "_blank")
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
        window.parent.proceed_payment(selectedInvoiceIds)
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

    return (
        <div>
            <DataGrid
                dataSource={ds}
                showBorders
                columnAutoWidth
                style={{height: '45vh'}}
                hoverStateEnabled={true}
                ref={refDataGrid}
                onToolbarPreparing={handleToolbarPreparing}
                remoteOperations={{ filtering: true }}
                allowColumnResizing={true}
                columnResizingMode="widget"
                showRowLines
                rowAlternationEnabled
                onRowDblClick={handleDbClick}
            >
                <Selection mode="multiple" />
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Scrolling mode="virtual" rowRenderingMode="virtual" />

                <Column type="buttons" width="80">
                    <CellButton icon="pdffile" onClick={handlePDFClick} />
                    <CellButton icon="showpanel" onClick={handleDetailClick} text="상세보기" />
                </Column>
                {/* <Column caption="#" cellRender={(a)=><div>{a.row.dataIndex+1}</div>} /> */}
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
                <Column dataField="partner_amount_pretax" visible={true}>
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="rrp_amount_pretax">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_amount_pretax">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_tax">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="paid">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="regId" />
                <Column dataField="regDate" />
                <Column dataField="stateCode" />
                <Column dataField="stateChgId" />
                <Column dataField="stateChgDate"/ >
                <Column dataField="remark" />
                <Summary>
                    <TotalItem column="seq" summaryType="count" valueFormat=",##0" />
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

export default React.memo(MainGrid);
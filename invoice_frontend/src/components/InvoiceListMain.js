import React, { useRef } from 'react';
import DataGrid, {
    Button as CellButton,
    Column,
    ColumnChooser,
    FilterRow,
    Scrolling,
    Selection,
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
            >
                <Selection mode="multiple" />
                <ColumnChooser enabled />
                <FilterRow visible={true} />
                <Scrolling mode="virtual" />

                <Column type="buttons" width="80">
                    <CellButton icon="pdffile" onClick={handlePDFClick} />
                    <CellButton icon="showpanel" onClick={handleDetailClick} />
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
        </div>
    );
}

export default React.memo(MainGrid);
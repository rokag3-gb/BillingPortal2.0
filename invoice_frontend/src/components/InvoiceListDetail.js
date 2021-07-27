import React, { useEffect } from 'react';
import DataGrid, {
    Scrolling,
    Summary,
    TotalItem,
    Column,
    Format,
} from 'devextreme-react/data-grid';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';

const urlInvoiceDetail = "/api/v1/invoice/detail/azure/"

function DetailGrid({ invoiceId }) {
    const store = new CustomStore({
        key: 'seq',
        load: function(loadOptions) {
            if (invoiceId === 0) { return }
            let params = "?"
            for (let i in loadOptions.filter) {
                params += `${loadOptions.filter[i].join("")}&`            
            }
            params = params.slice(0, -1);
            const url = urlInvoiceDetail + invoiceId + params
            return axios.get(url)
                .then((res) => {
                    console.log(`GET ${url} ok - len: ${res.data.results.length}`)
                    // return res.data.results
                    return res.data.results.map((data) => (
                        {
                            ...data,
                            partner_price: parseFloat(data.partner_price),
                            partner_amount: parseFloat(data.partner_amount),
                            rrp_price: parseFloat(data.rrp_price),
                            rrp_amount: parseFloat(data.rrp_amount),
                            our_price: parseFloat(data.our_price),
                            our_amount: parseFloat(data.our_amount)
                        }
                    ))
                })
                .catch((err) => {
                    console.log(err)
                    throw new Error("Load 실패")
                })
        }
    });
    const ds = new DataSource({store: store})
    return (
        <>
            <DataGrid
                showBorders
                columnAutoWidth
                dataSource={ds}
                remoteOperations={{ filtering: true }}
                style={{height: '50vh', paddingTop: 20}}
                allowColumnResizing={true}
                columnResizingMode="widget"
                showRowLines
                rowAlternationEnabled
            >
                <Scrolling mode="virtual" />
                <Column dataField="seq" />
                <Column dataField="orgId" />
                <Column dataField="invoiceId" />
                <Column dataField="orgName" />
                <Column dataField="vendorCode" />
                <Column dataField="vendorName" />
                <Column dataField="tenantId" />
                <Column dataField="subscriptionId" />
                <Column dataField="subscriptionName" />
                <Column dataField="sku" />
                <Column dataField="unit" />
                <Column dataField="chargeStartDate" />
                <Column dataField="chargeEndDate" />
                <Column dataField="orderId" />
                <Column dataField="region" />
                <Column dataField="serviceType" />
                <Column dataField="serviceName" />
                <Column dataField="resourceName" />
                <Column dataField="overageQuantity" />
                <Column dataField="currency" />
                <Column dataField="partner_price">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="partner_amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="rrp_price">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="rrp_amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_price">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="our_amount">
                    <Format type="fixedPoint" precision={2} />
                </Column>
                <Column dataField="vendorInvoiceId" />
                <Column dataField="billingCycleType" />
                <Column dataField="regDate" />
                <Summary>
                    <TotalItem column="seq" summaryType="count" valueFormat=",##0" />
                    <TotalItem column="partner_price" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="partner_amount" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="rrp_price" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="rrp_amount" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="our_price" summaryType="sum" valueFormat=",##0" />
                    <TotalItem column="our_amount" summaryType="sum" valueFormat=",##0" />
                </Summary>
            </DataGrid>
        </>
    )
}

export default React.memo(DetailGrid);
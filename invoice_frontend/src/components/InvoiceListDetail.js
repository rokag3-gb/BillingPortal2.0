import React, { useEffect } from 'react';
import DataGrid, {
    Scrolling,
    Summary,
    TotalItem,
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
                    return res.data.results
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
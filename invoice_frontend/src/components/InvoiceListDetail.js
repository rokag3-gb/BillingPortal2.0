import React, { useEffect } from 'react';
import DataGrid, {
    Scrolling,
} from 'devextreme-react/data-grid';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';

const urlInvoiceDetail = "/api/v1/invoice_azaz/"
const headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
}

const isEmpty = (val) => {
    return val === undefined || val === null || val === "";
}
const store = new CustomStore({
    key: 'seq',
    load: function(loadOptions) {
        if (isEmpty(loadOptions.filter)) {
            return
        }

        let params = "?"
        for (let i in loadOptions.filter) {
            if (loadOptions.filter[i][0] === "invoiceid" && loadOptions.filter[i][2] === 0) {
                return
            } else {
                params += `${loadOptions.filter[i].join("")}&`
            }
        }
        params = params.slice(0, -1);
        const url = urlInvoiceDetail + params

        return axios.get(url)
            .then((res) => {
                console.log(`GET ${url} ok - len: ${res.data.results.length}`)
                // console.log(res.data.results)
                return res.data.results
            })
            .catch((err) => {
                console.log(err)
                throw new Error("Load 실패")
            })
    },
    insert: function(values) {
        return axios.post(urlInvoiceDetail, values, { headers })
            .then((res) => {
                console.log(res.data)
            })
            .catch((err) => {
                console.log(err)
            })
    }
    
});

function DetailGrid({ invoiceId }) {
    const ds = new DataSource({store: store})

    useEffect(() => {
        ds.filter([
            ["invoiceid", "=", invoiceId],
            ["limit", "=", 1000],
        ])
        ds.load()
    }, [invoiceId])

    return (
        <>
            <DataGrid
                showBorders
                columnAutoWidth
                dataSource={ds}
                remoteOperations={{ filtering: true }}
                style={{height: '50vh', paddingTop: 20}}
            >
                <Scrolling mode="virtual" />
            </DataGrid>
        </>
    )
}

export default DetailGrid;
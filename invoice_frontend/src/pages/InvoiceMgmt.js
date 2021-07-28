import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CustomStore from 'devextreme/data/custom_store';
import DataSource from 'devextreme/data/data_source';
import InvoiceMgmtMain from '../components/InvoiceMgmtMain';
import InvoiceMgmtDetail from '../components/InvoiceMgmtDetail';
import GridToolbar from '../components/GridToolbar';
import * as utils from '../utils';

const initialSearchMonth = 3
const girdToolbarSize = 155
const urlInvoice = "/api/v1/invoice/"
const storeMain = new CustomStore({
    key: 'seq',
    load: function(loadOptions) {
        console.log("load main store")
        if (utils.isEmpty(loadOptions.filter)) {
            return
        }
        let params = "?"
        for (let i in loadOptions.filter) {
            params += `${loadOptions.filter[i].join("")}&`
        }
        params = params.slice(0, -1);
        const url = urlInvoice + params

        return axios.get(url)
            .then((res) => {
                console.log(`GET ${url} ok - len:${res.data.results.length}`)
                // return res.data.results
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
});
const dsMain = new DataSource({store: storeMain})

function InvoiceMgmt() {
    const [start, end] = utils.getDateSet(initialSearchMonth)
    const [invoiceId, setInvoiceId] = useState(0)
    const [startDate, setStartDate] = useState(start);
    const [endDate, setEndDate] = useState(end);
    const handleSearch = () => {
        dsMain.filter([
            ["invoiceDateStart", "=", utils.getDateFormat(startDate)],
            ["invoiceDateEnd", "=", utils.getDateFormat(endDate)],
            ["limit", "=", 10000],
        ])
        dsMain.load()
    }

    return (
        <div>
            <div style={{position: 'absolute', zIndex: 5}}>
                <GridToolbar
                    startDate={startDate}
                    setStartDate={setStartDate}
                    endDate={endDate}
                    setEndDate={setEndDate}
                    handleSearch={handleSearch}
                    girdToolbarSize={girdToolbarSize}
                />
            </div>
            <InvoiceMgmtMain ds={dsMain} setInvoiceId={setInvoiceId} />
            <InvoiceMgmtDetail invoiceId={invoiceId} />
        </div>
    )
}

export default InvoiceMgmt;

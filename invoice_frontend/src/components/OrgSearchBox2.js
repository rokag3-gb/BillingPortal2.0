import React, { useState } from 'react';
import DropDownBox from 'devextreme-react/drop-down-box';
import DataGrid, {
    Paging,
    FilterRow,
    Selection,
    Column,
} from 'devextreme-react/data-grid';
import CustomStore from 'devextreme/data/custom_store';

const dataSample = [
    {'orgId': 31, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 30, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 29, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 114, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 115, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 116, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 117, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 118, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 99, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 10, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 11, 'orgKey': 123, 'orgName': "org company"},
]
const ds = new CustomStore({
    key: 'orgId',
    load: () => {
        console.log("load")
        return dataSample
    }
})
function OrgSearchBox({ value, setValue }) {
    const [open, setOpen] = useState(false)
    const handleDropBoxOptionChanged = (e) => {
        if (e.name === "opened") {
            setOpen(e.value)
        }
    }
    const handleSelectionChanged = (e) => {
        setValue(e.selectedRowKeys[0])
        setOpen(false)
    }
    const gridRender = () => (
        <DataGrid
            dataSource={ds}
            hoverStateEnabled={true}
            columnAutoWidth
            height={200}
            onSelectionChanged={handleSelectionChanged}
        >
            <Paging enabled={false} />
            <Selection mode="single" />
            <FilterRow visible />
            
            <Column dataField="orgId" caption="ID" />
            <Column dataField="orgKey" caption="Key" />
            <Column dataField="orgName" cpation="Name" />
        </DataGrid>
    )
    return (
        <div style={{paddingLeft: 5}}>
            <DropDownBox
                width={100}
                placeholder="Org ID"
                value={value}
                //  deferRendering={false}
                // dataSource={ds}
                // dataSource={dataSample}
                //  displayExpr="orgId"
                contentRender={gridRender}
                opened={open}
                onOptionChanged={handleDropBoxOptionChanged}
            />
        </div>
    )
}

export default OrgSearchBox;
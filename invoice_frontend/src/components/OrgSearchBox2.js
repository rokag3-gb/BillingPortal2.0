import React from 'react';
import DropDownBox from 'devextreme-react/drop-down-box';
import DataGrid, { Paging, FilterRow, Selection } from 'devextreme-react/data-grid';

const dataSample = [
    {'orgId': 111, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 112, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 113, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 114, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 115, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 116, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 117, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 118, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 99, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 10, 'orgKey': 123, 'orgName': "org company"},
    {'orgId': 11, 'orgKey': 123, 'orgName': "org company"},
]

function OrgSearchBox({ value, onValueChanged }) {
    const gridRender = () => (
        <DataGrid
            dataSource={dataSample}
            hoverStateEnabled={true}
            columnAutoWidth
        >
            <Paging enabled={false} />
            <Selection mode="single" />
            <FilterRow visible />
        </DataGrid>
    )
    return (
        <div style={{paddingLeft: 5}}>
            <DropDownBox
                width={80}
                placeholder="orgIdg"
                value={value}
                //  deferRendering={false}
                dataSource={dataSample}
                //  displayExpr="orgId"
                contentRender={gridRender}
                dropdownOptions={
                    {width: 500}
                }
            />
        </div>
    )
}

export default OrgSearchBox;
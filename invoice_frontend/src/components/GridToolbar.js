import React, { useState, useEffect } from 'react';
import DateBox from 'devextreme-react/date-box';
import Button from 'devextreme-react/button';
import TextBox from 'devextreme-react/text-box';
import * as utils from '../utils';

function makeParam(startDate, endDate) {
    return `?invoiceDateStart=${startDate}&invoiceDateEnd=${endDate}&limit=10000`
}
const OrgBox = ({ onValueChanged }) => {
    return (
        <div style={{paddingLeft: 5}}>
            <TextBox onValueChanged={onValueChanged} width={80} placeholder="Org ID" />
        </div>
    )
}

function GridToolbar({startDate, setStartDate, endDate, setEndDate, setMainParam, girdToolbarSize, enableIdSearch=false}) {
    // const [windowSize, setWindowSize] = useState(window.innerWidth)
    // const handleResize = () => setWindowSize(window.innerWidth);
    const [orgId, setOrgId] = useState(0);
    const handleDateClick = (mm) => {
        const [start, end] = utils.getDateSet(mm)
        setStartDate(start)
        setEndDate(end)   
    }
    const handleSearch = () => {
        setMainParam(makeParam(utils.getDateFormat(startDate), utils.getDateFormat(endDate)))
    }
    useEffect(()=>{
        handleSearch()
        // window.addEventListener('resize', handleResize)
        // return () => {
        //     window.removeEventListener('resize', handleResize)
        // }
    },[])

    const tt = (e) => {
        console.log('hihi')
        setOrgId(e.value)
    }
    

    return (
        // <div style={{display: "flex", justifyContent: "space-between", width: (windowSize-girdToolbarSize)+'px'}}>
        <div style={{display: "flex", justifyContent: "space-between"}}>
            <div style={{display: "flex"}}>
                <DateBox
                    width={120}
                    value={startDate}
                    onValueChanged={(e)=>setStartDate(e.value)}
                    displayFormat="yyyy-MM-dd"
                />
                <DateBox
                    width={120}
                    value={endDate}
                    onValueChanged={(e)=>setEndDate(e.value)}
                    displayFormat="yyyy-MM-dd"
                />
                <Button text="3m" onClick={()=>handleDateClick(3)} />
                <Button text="6m" onClick={()=>handleDateClick(6)} />
                <Button text="12m" onClick={()=>handleDateClick(12)} />
                {enableIdSearch && <OrgBox onValueChanged={tt} />}
            </div>
            <div style={{paddingLeft: 5}}>
                <Button text="조회" onClick={handleSearch} />
            </div>
            {orgId}
        </div>
    );
}

export default GridToolbar;
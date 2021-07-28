import React, { useState, useEffect } from 'react';
import DateBox from 'devextreme-react/date-box';
import Button from 'devextreme-react/button';
import * as utils from '../utils';


function GridToolbar({startDate, setStartDate, endDate, setEndDate, handleSearch, girdToolbarSize}) {
    const [windowSize, setWindowSize] = useState(window.innerWidth)
    const handleDateClick = (mm) => {
        const [start, end] = utils.getDateSet(mm)
        setStartDate(start)
        setEndDate(end)   
    }
    const handleResize = () => setWindowSize(window.innerWidth);
    useEffect(()=>{
        handleSearch()
        window.addEventListener('resize', handleResize)
        return () => {
            window.removeEventListener('resize', handleResize)
        }
    },[])
    return (
        <div style={{display: "flex", justifyContent: "space-between", width: (windowSize-girdToolbarSize)+'px'}}>
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
            </div>
            <div>
                <Button text="조회" onClick={handleSearch} />
            </div>
        </div>
    );
}

export default GridToolbar;
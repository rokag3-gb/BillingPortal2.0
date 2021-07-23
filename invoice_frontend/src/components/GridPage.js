import React, { useState } from 'react';
import MainGrid from './MainGrid';
import DetailGrid from './DetailGrid';

function GridPage() {
    const [detailOrgId, setDetailOrgId] = useState(0)

    return (
        <>
            <MainGrid setDetailOrgId={setDetailOrgId} />
            <DetailGrid orgId={detailOrgId} />
        </>
    )
}

export default GridPage;

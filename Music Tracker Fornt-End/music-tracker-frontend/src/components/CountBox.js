import { useState, useEffect } from "react";

const RecentCount = (props) => {

    return (
        <>
            <div className="bg-gray-100 rounded-lg max-w-md p-2 m-4 shadow-md w-max">
                <p className="font-bold">{props.type} - {props.count}</p>
            </div>
            

        </>
    )
}

export default RecentCount;
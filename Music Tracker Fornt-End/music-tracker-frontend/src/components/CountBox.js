import { useState, useEffect } from "react";

const RecentCount = (props) => {
    console.log(props)

    return (
        <>
            <div className="bg-gray-100 rounded-lg max-w-md p-2 m-2 shadow-md w-4/5 place-items-center">
                <p className="font-bold">{props.type} - {props.count}</p>
            </div>
            

        </>
    )
}

export default RecentCount;
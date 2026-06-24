import { useState,useEffect } from "react";
import { useParams } from "react-router-dom";
import api from '../api/axios';

function ProjectDetails(){
    const {projectID} = useParams();
    const [qualityData,setQualityData] = useState(null)
    const [privacyData,setPrivacyDate] = useState(null)
    const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "20px"
}

const tableHeader = {
    border: "1px solid gray",
    padding: "10px",
    textAlign: "left",
    fontWeight: "bold"
}

const tableCell = {
    border: "1px solid gray",
    padding: "10px",
    textAlign: "left"
}


    const fetchQuality = async() => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.get(`/generator/quality/${projectID}/`,{headers:{Authorization : `Bearer ${token}`}})
            setQualityData(response.data)
        }
        catch(error){
            console.log(error)
        }

    
    }
    const fetchPrivacy = async() => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.get(`/generator/privacy/${projectID}/`,{headers:{Authorization:`Bearer ${token}`}})
            setPrivacyDate(response.data)
        }
        catch(error){
            console.log(error)
        }
    }
    const getRatingColor = (rating) => {
    switch(rating){
        case "Excellent":
            return "limegreen";
        case "Good":
            return "dodgerblue";
        case "Fair":
            return "orange";
        case "Poor":
            return "red";
        default:
            return "white";
    }
}
    useEffect(()=> {
        fetchQuality()
        fetchPrivacy()
    },[])
    return(
        <>
        <h1>Project Details</h1>
        <h2>Project ID: {projectID}</h2>
        
        <div
    style={{
        display: "flex",
        gap: "20px",
        marginTop: "20px",
        marginBottom: "20px"
    }}
>
      <div
    style={{
        border: `2px solid ${getRatingColor(
            qualityData?.quality_rating
        )}`,
        borderRadius: "10px",
        padding: "20px",
        minWidth: "200px"
    }}
>
    <h3>Quality Score</h3>

    <h1>{qualityData?.quality_score || 0}</h1>

    <p
        style={{
            color: getRatingColor(
                qualityData?.quality_rating
            )
        }}
    >
        {qualityData?.quality_rating}
    </p>
</div>
<div
    style={{
        border: `2px solid ${getRatingColor(
            privacyData?.privacy_rating
        )}`,
        borderRadius: "10px",
        padding: "20px",
        minWidth: "200px"
    }}
>
    <h3>Privacy Score</h3>

    <h1>{privacyData?.privacy_score || 0}</h1>

    <p
        style={{
            color: getRatingColor(
                privacyData?.privacy_rating
            )
        }}
    >
        {privacyData?.privacy_rating}
    </p>
</div>
</div>
<h2>Quality Metrics</h2>
<table style={tableStyle}>
    <thead>
        <tr>
            <th style={tableHeader}>Column</th>
            <th style={tableHeader}>Difference %</th>
            <th style={tableHeader}>Original Mean</th>
            <th style={tableHeader}>Synthetic Mean</th>
        </tr>
    </thead>

    <tbody>
        {qualityData?.quality_metrics &&
            Object.entries(
                qualityData.quality_metrics
            ).map(([column, metric]) => (
                <tr key={column}>
                    <td style={tableCell}>
                        {column}
                    </td>

                    <td style={tableCell}>
                        {metric.difference_percentage}
                    </td>

                    <td style={tableCell}>
                        {metric.original_mean}
                    </td>

                    <td style={tableCell}>
                        {metric.synthetic_mean}
                    </td>
                </tr>
            ))
        }
    </tbody>
</table>

<h2>Privacy Metrics</h2>

<table style={tableStyle}>
    <thead>
        <tr>
            <th style={tableHeader}>Metric</th>
            <th style={tableHeader}>Value</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td style={tableCell}>Total Synthetic Rows</td>
            <td style={tableCell}>
                {privacyData?.total_synthetic_rows || 0}
            </td>
        </tr>

        <tr>
            <td style={tableCell}>Duplicate Rows</td>
            <td style={tableCell}>
                {privacyData?.duplicate_rows || 0}
            </td>
        </tr>

        <tr>
            <td style={tableCell}>Duplicate Percentage</td>
            <td style={tableCell}>
                {privacyData?.duplicate_percentage || 0}%
            </td>
        </tr>

        <tr>
            <td style={tableCell}>Privacy Score</td>
            <td style={tableCell}>
                {privacyData?.privacy_score || 0}
            </td>
        </tr>

        <tr>
            <td style={tableCell}>Privacy Rating</td>
            <td style={tableCell}>
                {privacyData?.privacy_rating || "N/A"}
            </td>
        </tr>
    </tbody>
</table>
<h2>Categorical Metrics</h2>
{
    qualityData?.categorial_metrics &&
    Object.entries(
        qualityData.categorial_metrics
    ).map(([column, values]) => (

        <div
            key={column}
            style={{
                marginBottom: "20px"
            }}
        >
            <h3>{column}</h3>

            <table style={tableStyle}>
                <thead>
                    <tr>
                        <th style={tableHeader}>
                            Value
                        </th>

                        <th style={tableHeader}>
                            Original %
                        </th>

                        <th style={tableHeader}>
                            Synthetic %
                        </th>
                    </tr>
                </thead>

                <tbody>
{
    Object.keys(values.original).map(
        (key) => (
            <tr key={key}>
                <td style={tableCell}>
                    {key}
                </td>

                <td style={tableCell}>
                    {values.original[key]}
                </td>

                <td style={tableCell}>
                    {
                        values.synthetic[key] || 0
                    }
                </td>
            </tr>
        )
    )
}
</tbody>

            </table>

        </div>
    ))
}
        </>
    )
}
export default ProjectDetails;
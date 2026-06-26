import { useState,useEffect } from "react";
import { useParams } from "react-router-dom";
import api from '../api/axios';

function ProjectDetails(){
    const {projectID} = useParams();
    const [qualityData,setQualityData] = useState(null)
    const [privacyData,setPrivacyDate] = useState(null)
    const [downloadLink,setDownloadLink] = useState("")
    const [history,setHistory] = useState([]);
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
    const fetchDownloadLink =async() =>{
        try{
            const token = localStorage.getItem('access')
            const response = await api.get(`/dashboard/project/${projectID}/download/`,{headers: {Authorization:`Bearer ${token}`}})
            console.log(response.data)
            console.log('called')
            setDownloadLink(response.data.file)
        }
        catch(error){
            console.log(error)
        }
    }

    const fetchHistory =async()=>{
        try{
            const token = localStorage.getItem("access");
            const response = await api.get(`/generator/projects/${projectID}/history/`,{headers:{Authorization: `Bearer ${token}`}});
            setHistory(response.data)
        }
        catch(error){
            console.log(error)
        }
    }
    const downloadHistory = async (generationId) => {
    try {
        const token = localStorage.getItem("access");

        const response = await api.get(
            `/dashboard/download/${generationId}/`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        window.open(
            `http://127.0.0.1:8000${response.data.file}`,
            "_blank"
        );

    } catch (error) {
        console.log(error);
    }
};
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
        console.log("use effect")
        fetchQuality();
        fetchPrivacy();
        fetchDownloadLink();
        fetchHistory();
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
    qualityData?.categorical_metrics &&
    Object.entries(
        qualityData.categorical_metrics
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
{downloadLink && (
    <div style={{ marginTop: "30px" }}>
        <a
            href={`http://127.0.0.1:8000${downloadLink}`}download>
            <button>
                Download Synthetic Dataset
            </button>
        </a>
    </div>
)}
<h2>Generation History</h2>

{
    history.map((generation,index) => (
        <div
            key={generation.id}
            style={{
                border: "1px solid gray",
                padding: "15px",
                borderRadius: "10px",
                marginBottom: "15px"
            }}
        >
            <h3>Version {history.length - index}</h3>

            <p>Rows: {generation.rows_generated}</p>

            <p>Quality: {generation.quality_score}</p>

            <p>Privacy: {generation.privacy_score}</p>

            <p>{generation.created_at}</p>
            <button onClick={() => downloadHistory(generation.id)}>Download Version</button>
        </div>
    ))
}
        </>
    )
}
export default ProjectDetails;
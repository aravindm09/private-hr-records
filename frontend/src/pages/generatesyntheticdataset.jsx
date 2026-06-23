import {useState,useEffect} from 'react'
import { useNavigate,useParams } from 'react-router-dom'
import api from '../api/axios'

function GenerateSyntheticDataset(){
    const [rows,setRows]= useState(100)
    const [loading,setLoading]= useState(false)
    const [privacyLevel,setPrivacyLevel] = useState("medium")
    const [message,setMessage]= useState("")
    const [downloadLink,setDownloadLink]= useState("")
    const{projectID}= useParams()


    const handleGenerate = async() => {
        try{
            setLoading(true)
            const token = localStorage.getItem("access")
            const response = await api.post(`generator/synthetic/${projectID}/`,{rows: Number(rows),privacy_level:privacyLevel},{headers:{Authorization: `Bearer ${token}`}})
            setMessage(response.data.message)
            setDownloadLink(response.data.file)
        }
        catch(error){
            console.log(error)
        }
        finally{
            setLoading(false)
        }
    }

    return(
        <>
        <h1>Generate Synthetic Dataset</h1>
        <input type='number' value={rows} onChange={(e)=> setRows(e.target.value)}/>
        <label>Privacy Level</label>
        <select value={privacyLevel} onChange={(e)=> setPrivacyLevel(e.target.value)}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
        </select>
        <button onClick={handleGenerate} disabled={loading}>{loading ? "Generating":"Generate"}</button>
        {message && ( 
            <p>{message}</p>
        )}
        {downloadLink && (
            <a href={`http://127.0.0.1:8000${downloadLink}`} target='_blank' rel='noreferrer'>Download Synthethic CSV</a>
        )}
        </>
    )
}
export default GenerateSyntheticDataset
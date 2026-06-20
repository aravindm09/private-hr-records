import api from "../api/axios"
import { useNavigate,useParams } from "react-router-dom"
import { useState,useEffect } from "react"

function Generator(){
    const [rows, setRows] =useState([])
    const [row_count, setRow_count] = useState("10")
    const navigate = useNavigate()
    const {projectID}=useParams()
    const [loading, setLoading]=useState(false)

    const handleGenerate = async() =>{
        try { setLoading(true)
            const token = localStorage.getItem("access")
            const response = await api.post(`generator/generate/${projectID}/`,{rows: Number(row_count)},{headers:{Authorization: `Bearer ${token}`}})
            console.log(response.data)
            setRows(response.data)
            setLoading(false)
        }
        catch(error){
            console.log(error)
            setLoading(false)
        }
        finally{
            setLoading(false)
        }
    }
    return(
        <>
        <h1>generate page</h1>
        <input type="number" placeholder="Row count" value={row_count} onChange={(e)=>setRow_count(e.target.value)}/>
        {rows.map((row,index)=>
        <pre key={index}>
             {JSON.stringify(row,null,2)}
        </pre>)}
        <button disabled={loading} onClick={(e)=>{handleGenerate()}}>{loading ? "Generating":"Generate"} </button>
        </>
    )
}

export default Generator
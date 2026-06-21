import {useParams} from 'react-router-dom';
import {useState} from 'react';
import api from "../api/axios"


function UploadDataset(){
    const [file,setFile] = useState(null)
    const [dataset,setDataset]= useState(null)
    const [preview,setPreview]=useState([])
    const [fields,setFields]=useState([])
    const {projectID}= useParams()
    const[loading,setLoading]=useState(false)
    const handleUpload = async() => {
        setLoading(true)
        const formData = new FormData()
        if(!file){
            alert('Please select a CSV file')
            return
        }
        formData.append("file",file)
        try {

            const token = localStorage.getItem("access")
            const response = await api.post(`uploads/upload/${projectID}/`,formData,{headers:{Authorization:`Bearer ${token}`}})
            setDataset(response.data.dataset)
            setPreview(response.data.preview)
            setFields(response.data.fields)
            console.log(response.data)
            
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
        <input type='file' accept='.csv' onChange={(e)=> setFile(e.target.files[0])}/>
        <button disabled={loading} onClick={handleUpload}>{loading ? "Uploading...":"Upload CSV"}</button>
        {dataset && (
            <>
            <h3>
                Dataset Info
            </h3>
            <p>Rows: {dataset.row_count}</p>
            <p>Columns : {dataset.column_count}</p>
            </>
        )}
        {fields.length>0 && (
            <>
            <h3>Detected Fields</h3>
            {fields.map((field,index)=> <div key={index}>
                {field.field_name} - {field.field_type}
            </div>)}</>
        )}
        {preview.map((row,index)=>(
            <pre key={index}>
                {JSON.stringify(row,null,2)}
            </pre>
        ))}
        </>
    )
}
export default UploadDataset
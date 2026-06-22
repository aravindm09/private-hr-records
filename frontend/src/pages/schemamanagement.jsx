import { useEffect, useState } from "react"
import {useNavigate,useParams} from 'react-router-dom';
import api from '../api/axios';

function SchemaManagement(){
    const {projectID} = useParams()
    const [field,setField] = useState([])
    const [loading,setLoading] = useState(false)

    useEffect(()=> {
        fetchfields()
    },[])

    const fetchfields = async () =>{
        try{
            const token = localStorage.getItem('access')
            console.log("token =",token)
            const response = await api.get(`datasets/list/${projectID}/`,{headers:{Authorization: `Bearer ${token}`}})
            setField(response.data)
        }
        catch(error){
            console.log(error)
        }
    }

    const handleChange = (index,fieldName,value)=>{
        const updated_fields =[...field]
        updated_fields[index][fieldName]= value
        setField(updated_fields)
    }

    const handleSave = async(fieldID,fieldData) =>{ console.log(fieldData)
        try{
        const token = localStorage.getItem('access')
        const response = await api.put(`datasets/fields/${fieldID}/`,{"field_type": fieldData.field_type,"generation_method":fieldData.generation_method},{headers:{Authorization: `Bearer ${token}`}})
        alert("saved successfully")
        console.log(response.data)
    }
    catch(error){
        console.log(error)
    }}

    return(
        <>
        <h1>Schema management</h1>
        {field.map((field,index)=>
        (
            <div key={field.id} 
            style={{
                border: "1px solid grey",
                margin: "10px",
                padding:"10px"
           }}>
                <h4>{field.field_name}</h4>
                <label>Field Type</label>
                <select value={field.field_type} onChange={(e)=> handleChange(index,"field_type",e.target.value)}>
                    <option value="string">String</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                    <option value="email">Email</option>
                    <option value="boolean">Boolean</option>
                </select>
                <br />
                <br />
                <label> Generation Method</label>
                <select value={field.generation_method} onChange={(e)=> handleChange(index,"generation_method",e.target.value)}>
                    <option value="ctgan">CTGAN</option>
                    <option value="faker">Faker</option>
                    <option value="ignore">Ignore</option>
                </select>
                <br />
                <br />
                <button onClick={()=> handleSave(field.id,field)}>save</button>
            </div>
        ))}
        </>
    )

}
export default SchemaManagement
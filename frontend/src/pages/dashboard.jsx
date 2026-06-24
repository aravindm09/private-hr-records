import api from "../api/axios"
import {useNavigate,} from "react-router-dom"
import {useState,useEffect} from "react"

function Dashboard() {
    const navigate = useNavigate()
    const [projects, setProjects] = useState([])
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [editId, setEditId] = useState(null)
    const [dashboardStats,setDashboardStats] = useState(null)

    const fetchProjects = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.get("/projects/list/", { headers: { Authorization: `Bearer ${token}` } })
            setProjects(response.data)
            console.log(projects)
        } catch (error) {
            console.log(error)
        }
    }

    const fetchDashboardStats = async() =>{
        try{
            const token = localStorage.getItem("access")
            const response = await api.get(`/dashboard/stats/`,{headers:{Authorization:`Bearer ${token}`}})
            console.log(response.data)
            setDashboardStats(response.data)
        }
        catch(error){
            console.log(error)
        }
    }
        
    useEffect(() => {
        fetchProjects(),
        fetchDashboardStats()
    }, [])

   

    const handleCreateProject = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.post("/projects/create/", { name, description }, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            fetchProjects()
            fetchDashboardStats() // Refresh the project list
            setName("")
            setDescription("")
        } catch (error) {
            console.log(error)
        }
    }

    const handleDeleteProject = async (Id) => {
        try{
            const token = localStorage.getItem("access")
            const response = await api.delete(`/projects/${Id}/delete/`, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            await fetchProjects()
            await fetchDashboardStats() // Refresh the project list 
        } catch (error) {
            console.log(error)
        }
    }
    const handleGetProfile = async () => {

        try {

            const token =
                localStorage.getItem("access")

            const response =
                await api.get(
                    "/accounts/profile/",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            console.log(
                response.data
            )

        }
        catch(error) {

            console.log(error)

        }
    }
    const handleUpdateProject = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.patch(`/projects/${editId}/update/`, { name, description }, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            fetchProjects()
            fetchDashboardStats() // Refresh the project list 
            setName("")
            setDescription("")
            setEditId(null)
        } catch (error) {
            console.log(error)
        }
    }
    const handleEditProject = ( project) => { setName(project.name),setDescription(project.description),setEditId(project.id)}
    const handlelogout = () => {
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
        navigate("/login")
    }

    return (
        <>
            <h1>Dashboard Page</h1>
            <div style={{display: "flex",gap: "20px",marginBottom:"20px"}}>
                <div style={{border:"1px solid grey", padding:"20px", borderRadius:"10px"}}><h3>Projects</h3>
                <p>{dashboardStats?.total_projects || 0}</p></div>
                 <div style={{border:"1px solid grey", padding:"20px", borderRadius:"10px"}}><h3>Quality Score</h3>
                <p>{dashboardStats?.average_quality_score || 0}</p></div>
                 <div style={{border:"1px solid grey", padding:"20px", borderRadius:"10px"}}><h3>Privacy Score</h3>
                <p>{dashboardStats?.average_privacy_score || 0 }</p></div>
                 <div style={{border:"1px solid grey", padding:"20px", borderRadius:"10px"}}><h3>Datasets</h3>
                <p>{dashboardStats?.total_datasets || 0}</p></div>
            </div>

            <button
                onClick={handleGetProfile}
            >
                Get Profile
            </button>
            <button onClick={() => handlelogout()}>
                Logout
            </button>
            <div
    style={{
        border:"1px solid gray",
        borderRadius:"10px",
        padding:"20px",
        width:"500px",
        marginBottom:"20px"
    }}>
         <input
                type="text"
                placeholder="Project Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <input 
                type="text"
                placeholder="Project Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <button
        onClick={editId ? handleUpdateProject : handleCreateProject}>
                {editId ? "Update Project" : "Create Project"}
            </button>

    </div>
     <h2>Recent Projects</h2>
           <div>
    {projects.map((project) => (
        <div
            key={project.id}
            style={{
                border: "1px solid gray",
                padding: "15px",
                borderRadius: "10px",
                marginBottom: "15px"
            }}
        >
            <h3>{project.name}</h3>

            <p>{project.description}</p>

            <button onClick={() =>navigate(`/projects/${project.id}`)}>Open</button>

            <button onClick={() =>handleEditProject(project)}>Edit</button>

            <button onClick={() =>handleDeleteProject(project.id)}>Delete</button>

        </div>
    ))}
</div>         
        </>
    )
}

export default Dashboard
import type { PlanItem,AddResponse } from "@/types/train";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


export const Train_api={
    async add(token:string,planForm:PlanItem):Promise< AddResponse>{
        const response= await fetch(`${API_BASE_URL}/api/training-plan`, {
            method: 'POST',
            headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(planForm)
        })

        if (!response.ok){
            throw '提交失败'
        }

        return response.json()
    }
}

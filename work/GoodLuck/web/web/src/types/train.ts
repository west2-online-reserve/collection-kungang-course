export interface PlanItem{
    "id"?: number,
    "date": string,
    "project": string,
    "target": number,
    "note": string,
    "completed"?: boolean,
    "actualCount"?: number
}

export interface  AddResponse{
    'code': number,
    'message': string,
    'data': PlanItem
}



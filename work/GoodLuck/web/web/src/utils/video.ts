import type{ TeachingVideo,VideoResponse } from '@/types/video'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const videoApi={
  async fetch_all_videos(token:string):Promise<VideoResponse<TeachingVideo[]>>{
    const response = await fetch(`${API_BASE_URL}/api/media/videos`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'

      }
    });
    if (!response.ok){
      throw 'fetch exxample videos error'
    }

    return response.json()
  }
}

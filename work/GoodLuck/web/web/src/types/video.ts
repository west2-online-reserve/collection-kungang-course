export interface TeachingVideo {
  id: number
  title: string
  thumbnail: string
  url: string
  duration: string
}
export interface VideoResponse<T> {
  code: number;
  message: string;
  data: T
}

'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import PostCard from "./PostCard"
import { stringify } from 'postcss'

export default function LinkedInPostIdeas() {
  const [ideas, setIdeas] = useState([])
  const [loading, setLoading] = useState(false)

  const generateIdeas = async () => {
    setLoading(true)
    try {
      let response = await fetch(`/api/FetchIdeas`, {
        method: "GET",
      })
      let data = await response.json()
      console.log(data.body)
      let final_ideas_list = data.body
 
      console.log("type of ideas_list:", typeof final_ideas_list) // Should be "object" if parsed correctly
    //   console.log("ideas_list:", final_ideas_list) // Should be an array if parsed correctly
      
      setIdeas(final_ideas_list) // Set the ideas state with the fetched data
    } catch (error) {
      console.log("Error fetching ideas:", error)
    } finally {
      setLoading(false)
    }
  }
  

  useEffect(() => {
    console.log("Updated ideas:", ideas)
  }, [ideas])

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-900 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center text-white">LinkedIn Post Ideas Generator</h1>
        <div className="flex flex-col items-center mb-8 space-y-4">
          <Button
            onClick={generateIdeas}
            className="bg-gradient-to-r from-pink-500 to-purple-500 text-white font-bold py-2 px-6 rounded-full"
          >
            {loading ? "Loading..." : "Generate Ideas"}
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {
          Array.isArray(ideas) && ideas.length > 0 
          ? (
            ideas.map((idea, index) => {
              console.log("Rendering PostCard with idea:", idea) // Log each idea being passed to PostCard
              return <PostCard key={index} ideas={idea} />
            })
          ) : (
            !loading && <p className="text-white text-center col-span-full">No ideas available. Click "Generate Ideas" to fetch some!</p>
          )}
        </div>
      </div>
    </div>
  )
}

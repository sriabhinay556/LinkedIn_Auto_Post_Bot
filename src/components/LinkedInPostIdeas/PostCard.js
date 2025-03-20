'use client'

import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Heart, MessageCircle, Share2 } from 'lucide-react'
import { Button } from "@/components/ui/button"

export default function PostCard({ ideas }) {
  return (
    <Card className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-xl overflow-hidden border border-gray-200 border-opacity-20 hover:shadow-2xl transition-all duration-300">
      <CardContent className="p-3">
        <p className="text-white text-lg mb-4">
          {ideas.hook}
          <span className="text-sm m-2 p-1 rounded-md bg-gradient-to-br from-green-400 to-purple-500">
            {ideas.category}
          </span>
        </p>

        {/* Scrollable content container */}
        <div className="p-2 h-60 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg mb-4 overflow-y-auto">
          <p className="text-white whitespace-pre-line">{ideas.body}</p>
        </div>
      </CardContent>
      {/* <CardFooter className="bg-black bg-opacity-30 p-4 flex justify-between">
        <Button variant="ghost" size="icon"><Heart className="text-white hover:text-pink-500 h-6 w-6" /></Button>
        <Button variant="ghost" size="icon"><MessageCircle className="text-white hover:text-blue-500 h-6 w-6" /></Button>
        <Button variant="ghost" size="icon"><Share2 className="text-white hover:text-green-500 h-6 w-6" /></Button>
      </CardFooter> */}
    </Card>
  )
}

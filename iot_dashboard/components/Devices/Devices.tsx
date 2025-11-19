"use client"

import { Label } from "@radix-ui/react-label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card"
import { Input } from "../ui/input"
import { Button } from "../ui/button"

export default function Devices() {
  return (
    <div className="grid grid-cols-4 gap-5">
      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Kitchen
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            Kitchen
          </div>
          <div className="text-2xl font-bold">
            Dishwasher
          </div>
          <div className="text-2xl font-bold">
            Microwave
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Climate & Heating
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            Furnace 1
          </div>
          <div className="text-2xl font-bold">
            Furnace 2
          </div>
          <div className="text-2xl font-bold">
            Living room
          </div>
          <div className="text-2xl font-bold">
            Home office
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Refrigeration
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            Fridge
          </div>
          <div className="text-2xl font-bold">
            Wine cellar
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Outdoor
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            Barn
          </div>
          <div className="text-2xl font-bold">
            Well
          </div>
          <div className="text-2xl font-bold">
            Garage
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
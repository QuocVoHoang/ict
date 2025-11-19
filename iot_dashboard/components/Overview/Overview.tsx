"use client"

import { Label } from "@radix-ui/react-label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card"
import { Input } from "../ui/input"
import { Button } from "../ui/button"

export default function Overview() {
  return (
    <div className="grid grid-cols-4 gap-5">
      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Total electricity usage
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            5 Kwh
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Electricity generated
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            5 Kwh
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Temperature
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            22°C
          </div>
        </CardContent>
      </Card>

      <Card className="bg-white/5 backdrop-blur-md border border-white/30 text-white">
        <CardHeader className="font-semibold">
          Humidity
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            10%
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
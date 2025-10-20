import Link from "next/link"
import Image from "next/image"
import { ArrowLeftIcon } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ThemeToggle } from "@/components/theme-toggle"
import { StrategicTickers } from "@/components/strategic-tickers"
import { ReportDetailView } from "@/components/report-detail-view"

export default async function ReportDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="hover:opacity-80 transition-opacity">
                <Image
                  src="/cyberlogix-logo.jpeg"
                  alt="CyberLogix.ai"
                  width={240}
                  height={44}
                  className="h-11 w-auto"
                />
              </Link>
              <Link
                href="/"
                className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors border-l pl-4"
              >
                <ArrowLeftIcon className="h-4 w-4" />
                Back to Reports
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
              <div className="flex items-center gap-3">
                <Avatar className="h-9 w-9">
                  <AvatarImage src="/professional-executive-manager-portrait.jpg" alt="Janusz Trucker" />
                  <AvatarFallback>JT</AvatarFallback>
                </Avatar>
                <div className="text-right">
                  <p className="text-sm font-medium text-foreground">Janusz Trucker</p>
                  <p className="text-xs text-muted-foreground">Operations Manager</p>
                  <p className="text-xs text-muted-foreground">Big Trucking Corp Ltd. • NIP: 314159265</p>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-border">
            <StrategicTickers />
          </div>
        </div>
      </header>

      {/* Report Content - Now using real backend data */}
      <ReportDetailView reportId={id} />
    </div>
  )
}

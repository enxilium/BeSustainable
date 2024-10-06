import "@/styles/globals.css";
import PageTransition from '@/components/PageTransition';
import StairTransition from '@/components/StairTransition';
import Header from '@/components/Header';
import { Cutive_Mono } from 'next/font/google';

const cutiveMono = Cutive_Mono({
  subsets: ['latin'],
  weight: ["400"],
  variable: "--font-cutivemono",
})

export const metadata = {
  title: "EcoCloset",
  description: "Sustainable Fashion"
}

const BaseLayout = ({children}) => {
  
  return (
    <html lang="en">
      <body className={cutiveMono.variable}>
        <Header class="z-50"/>
        <StairTransition></StairTransition>
        <PageTransition>
          {children}
        </PageTransition>
      </body>
    </html>
  )
}

export default BaseLayout;